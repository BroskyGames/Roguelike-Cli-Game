from random import Random

from .state import GameState

class GameEngine:
    def __init__(self, state: GameState) -> None:
        self.rng = Random(state.seed)
        self.state = state

        if state.rng_state is not None:
            self.rng.setstate(state.rng_state)

        if self.state.debug:
            print(f"Seed: {state.seed}")