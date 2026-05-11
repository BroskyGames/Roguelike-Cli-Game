from copy import deepcopy
from random import Random
from typing import Any

from game.core.geometry import Pos
from game.core.logger import Logger
from game.core.router import Router
from game.core.scheduler import Task, TaskScheduler
from game.core.state import Phase, State
from game.domain.actions import (
    Action,
    AttackAction,
    ClearQueueAction,
    EndTurnAction,
    MoveAction,
    RemoveLastAction,
    WaitAction,
)
from game.ecs.managers.entity_lifecycle_manager import EntityLifecycleManager
from game.ecs.managers.room_manager import RoomManager
from game.ecs.managers.trigger_lifecycle_manager import TriggerLifecycleManager
from game.ecs.managers.turn_managers import AITurnManager, PlayerTurnManager
from game.ecs.systems.compute_processor import ComputeProcessor
from game.ecs.systems.field_of_view_processor import FieldOfViewProcessor
from game.ecs.systems.movement_handler import MovementHandler
from game.ecs.systems.player_action_queue_service import PlayerActionQueueService
from game.ecs.systems.trigger_processor import TriggerProcessor


class Engine:
    __slots__ = [
        "rng",
        "state",
        "logger",
        "_router",
        "_processors",
        "_scheduler",
        "_turn_queue",
        "_entity_manager",
        "_trigger_manager",
        "_room_manager",
        "_action_queue",
    ]

    def __init__(self, state: State) -> None:
        # RNG
        self.rng = Random(state.seed)
        self.state = state

        if state.rng_state is not None:
            self.rng.setstate(state.rng_state)

        if self.state.debug:
            print(f"Seed: {state.seed}")

        self.logger = Logger(100)

        # Processing
        self._router = Router()

        self._processors: dict[str, Any] = {
            "fov_processor": FieldOfViewProcessor(self.state.context),
            "move_processor": MovementHandler(self.state.context),
            "trigger_processor": TriggerProcessor(self.state.context),
        }

        self._scheduler = TaskScheduler()
        self._turn_queue: list[tuple[Task, bool]] = [
            (PlayerTurnManager(self._router), False),
            (ComputeProcessor(self.state.context), True),
            (
                AITurnManager(
                    self._router,
                    self.state.context,
                    self.rng,
                    self._processors["move_processor"],
                    self.logger,
                ),
                False,
            ),
        ]
        self._entity_manager = EntityLifecycleManager(self.state.context)
        self._trigger_manager = TriggerLifecycleManager(self.state.context)
        self._room_manager = RoomManager(
            self.state.context, self._trigger_manager, self._entity_manager
        )

        self._router.register(MoveAction, self._processors["move_processor"].process)
        self._router.register(MoveAction, self._processors["fov_processor"].process)
        self._router.register(
            AttackAction, lambda a: self.logger.add(f"Entity {a.ent} attacked")
        )
        self._router.register(WaitAction, lambda _: None)

    def __eq__(self, other):
        if not isinstance(other, Engine):
            return False
        if self.state != other.state:
            return False
        if self.rng.getstate() != other.rng.getstate():
            return False
        return True

    def get_save(self) -> State:
        self.state.rng_state = self.rng.getstate()
        return deepcopy(self.state)

    # --- Engine Logic ---
    def start(self):
        self._action_queue = PlayerActionQueueService(self.state.context.player)
        self._processors["fov_processor"].process_all()
        self._room_manager.init_rooms()

    def handle_actions(self, action: Action) -> None:
        if self.state.phase == Phase.PLANNING:
            match action:
                case EndTurnAction():
                    self.state.phase = Phase.RESOLUTION
                    for item, instant in self._turn_queue:
                        self._scheduler.add(item, instant)

                case RemoveLastAction():
                    self._action_queue.remove_last()

                case ClearQueueAction():
                    self._action_queue.clear()

                case Action():
                    self._action_queue.add(action)

    def execute_step(self) -> bool:
        working = self._scheduler.step()
        self._processors["trigger_processor"].process()

        if not working:
            self.state.phase = Phase.PLANNING

        return working

    # --- Engine API ---
    def create_entity(self, pos: Pos, *components) -> int:
        ent = self._entity_manager.create(pos, *components)
        return ent
