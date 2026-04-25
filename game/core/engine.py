from random import Random

from game.core.router import Router
from game.core.scheduler import ProcessorScheduler
from game.core.state import Phase, State
from game.domain.actions import Action, ClearQueueAction, EndTurnAction, MoveAction, RemoveLastAction
from game.systems.action_queue_processor import ActionQueueProcessor
from game.systems.ap_processor import ActionPointsProcessor
from game.systems.field_of_view_processor import FieldOfViewProcessor
from game.systems.movement_processor import MovementProcessor
from game.systems.turn_processors import PlayerTurnProcessor, StepProcessor


class Engine:
    def __init__(self, state: State) -> None:
        # RNG
        self.rng = Random(state.seed)
        self.state = state

        if state.rng_state is not None:
            self.rng.setstate(state.rng_state)

        if self.state.debug:
            print(f"Seed: {state.seed}")

        # Routing
        self.router = Router()
        self.router.register(MoveAction, MovementProcessor(self.state.context).process)

        # Processors
        self.turn_processors: list[StepProcessor] = [
            PlayerTurnProcessor(self.router),
            # EnemyTurnProcessor(self.router),
        ]
        self.ap_processor = ActionPointsProcessor()
        self.action_queue = ActionQueueProcessor()
        self.fov_processor = FieldOfViewProcessor(self.state.context)
        self.scheduler = ProcessorScheduler()

        self.fov_processor.process()

    def get_save(self):
        self.state.rng_state = self.rng.getstate()
        return self.state

    def handle_actions(self, action: Action) -> None:
        if self.state.phase == Phase.PLANNING:
            match action:
                case EndTurnAction():
                    self.state.phase = Phase.RESOLUTION
                    for processor in self.turn_processors:
                        self.scheduler.add(processor)
                    self.scheduler.start()
                case RemoveLastAction():
                    self.action_queue.remove_last()
                case ClearQueueAction():
                    self.action_queue.clear()
                case Action():
                    self.action_queue.add(action)

    def execute_step(self) -> bool:
        working = self.scheduler.step()
        self.fov_processor.process()

        if not working:
            self.state.phase = Phase.PLANNING
            self.ap_processor.reset_all()

        return working
