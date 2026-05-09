from copy import deepcopy
from random import Random
from typing import Any

from game.core.geometry import Pos
from game.core.router import Router
from game.core.scheduler import TaskScheduler
from game.core.state import Phase, State
from game.domain.actions import (
    Action,
    ClearQueueAction,
    EndTurnAction,
    MoveAction,
    RemoveLastAction,
)
from game.ecs.managers.action_queue_manager import ActionQueueManager
from game.ecs.managers.entity_lifecycle_manager import EntityLifecycleManager
from game.ecs.managers.room_manager import RoomManager
from game.ecs.managers.trigger_manager import TriggerManager
from game.ecs.managers.turn_managers import PlayerTurnManager, StepProcessor
from game.ecs.systems.field_of_view_processor import FieldOfViewProcessor
from game.ecs.systems.movement_processor import MovementProcessor
from game.ecs.systems.trigger_processor import TriggerProcessor


class Engine:
    def __init__(self, state: State) -> None:
        # RNG
        self.rng = Random(state.seed)
        self.state = state

        if state.rng_state is not None:
            self.rng.setstate(state.rng_state)

        if self.state.debug:
            print(f"Seed: {state.seed}")

        # Processing
        self._router = Router()

        self._scheduler = TaskScheduler()
        self._turn_queue: list[StepProcessor] = [
            PlayerTurnManager(self._router),
            # EnemyTurnProcessor(self.router),
        ]
        self._action_queue = ActionQueueManager()
        self._entity_lifecycle = EntityLifecycleManager(self.state.context)
        self._trigger_manager = TriggerManager()
        self._room_manager = RoomManager(
            self.state.context, self._trigger_manager, self._entity_lifecycle
        )

        self._processors: dict[str, Any] = {
            "fov_processor": FieldOfViewProcessor(self.state.context),
            "move_processor": MovementProcessor(self.state.context),
            "trigger_processor": TriggerProcessor(),
        }

        self._router.register(MoveAction, self._processors["move_processor"].process)
        self._router.register(MoveAction, self._processors["fov_processor"].process)

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
        self._processors["fov_processor"].process_all()
        self._room_manager.init_rooms()

    def handle_actions(self, action: Action) -> None:
        if self.state.phase == Phase.PLANNING:
            match action:
                case EndTurnAction():
                    self.state.phase = Phase.RESOLUTION
                    for item in self._turn_queue:
                        self._scheduler.add(item)
                    self._scheduler.start()

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
        ent = self._entity_lifecycle.create(pos, *components)
        return ent
