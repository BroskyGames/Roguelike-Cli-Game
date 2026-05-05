from copy import deepcopy
from random import Random

from game.core.router import Router
from game.core.scheduler import ProcessorScheduler
from game.core.state import Phase, State
from game.domain.actions import Action, ClearQueueAction, EndTurnAction, MoveAction, RemoveLastAction
from game.ecs.managers.action_queue_manager import ActionQueueManager
from game.ecs.managers.turn_managers import PlayerTurnManager, StepProcessor
from game.ecs.systems.field_of_view_processor import FieldOfViewProcessor
from game.ecs.systems.movement_processor import MovementProcessor


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
        self.router = Router()

        self.scheduler = ProcessorScheduler()
        self.turn_queue: list[StepProcessor] = [
            PlayerTurnManager(self.router),
            # EnemyTurnProcessor(self.router),
        ]
        self.action_queue = ActionQueueManager()

        self.processors = {
            "fov_processor": FieldOfViewProcessor(self.state.context),
            "move_processor": MovementProcessor(self.state.context),
        }

        self.router.register(MoveAction, self.processors["move_processor"].process)
        self.router.register(MoveAction, self.processors["fov_processor"].process)

        self.processors["fov_processor"].process_all()

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

    def handle_actions(self, action: Action) -> None:
        if self.state.phase == Phase.PLANNING:
            match action:
                case EndTurnAction():
                    self.state.phase = Phase.RESOLUTION
                    for item in self.turn_queue:
                        self.scheduler.add(item)
                    self.scheduler.start()

                case RemoveLastAction():
                    self.action_queue.remove_last()

                case ClearQueueAction():
                    self.action_queue.clear()

                case Action():
                    self.action_queue.add(action)

    def execute_step(self) -> bool:
        working = self.scheduler.step()

        if not working:
            self.state.phase = Phase.PLANNING

        return working
