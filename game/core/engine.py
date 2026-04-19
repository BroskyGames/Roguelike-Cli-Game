from random import Random

import esper

from game.core.router import Router
from game.core.state import Phase, State
from game.domain.components import ActionPoints
from game.systems.turn_processors import EnemyTurnProcessor, PlayerTurnProcessor, StepProcessor


class Engine:
    def __init__(self, state: State) -> None:
        self.rng = Random(state.seed)
        self.state = state
        self.router = Router()
        self.turn_processors: list[StepProcessor] = [
            PlayerTurnProcessor(self.router),
            EnemyTurnProcessor(self.router),
        ]

        if state.rng_state is not None:
            self.rng.setstate(state.rng_state)

        if self.state.debug:
            print(f"Seed: {state.seed}")

    def get_save(self):
        self.state.rng_state = self.rng.getstate()
        return self.state

    def handle_input(self, key: int) -> None:
        if self.state.phase == "PLANNING":
            match key:
                case ord("\n"):
                    self.state.phase = Phase.RESOLUTION
                    for processor in self.turn_processors:
                        processor.start_processor()

    def execute_step(self) -> bool:
        for processor in self.turn_processors:
            processor.process()

        return any(processor.working for processor in self.turn_processors)

    @staticmethod
    def reset_ap() -> None:
        for ent, ap in esper.get_component(ActionPoints):
            ap.current = ap.max
