from collections.abc import Generator
from random import Random

import esper

from game.core.state import Phase, State
from game.systems.components import ActionPoints


def any_ap_remaining() -> bool:
    return any(
        ap.current > 0
        for _, ap in esper.get_component(ActionPoints)
        # if esper.has_component(_, IsPlayer) or esper.has_component(_, AI)
    )


class Engine:
    def __init__(self, state: State) -> None:
        self.rng = Random(state.seed)
        self.state = state
        self._turn_executor = None

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
                    self._turn_executor = self._make_turn_executor()
                    self.state.phase = Phase.RESOLUTION

    @staticmethod
    def reset_ap() -> None:
        for ent, ap in esper.get_component(ActionPoints):
            ap.current = ap.max

    def _make_turn_executor(self) -> Generator[None, None, None]:
        while any_ap_remaining():
            esper.process()
            yield

        self.state.phase = Phase.PLANNING
        self.reset_ap()

    def execute_step(self) -> bool:
        assert self._turn_executor is not None, "Called execute_step outside of resolution phase"

        try:
            next(self._turn_executor)
            return False
        except StopIteration:
            self._turn_executor = None
            return True
