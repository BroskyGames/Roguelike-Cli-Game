from random import Random

from .state import State


class Engine:
    def __init__(self, state: State) -> None:
        self.rng = Random(state.seed)
        self.state = state

        if state.rng_state is not None:
            self.rng.setstate(state.rng_state)

        if self.state.debug:
            print(f"Seed: {state.seed}")

    def get_save(self):
        self.state.rng_state = self.rng.getstate()
        return self.state

    def handle_input(self, key: int) -> None:
        ...
