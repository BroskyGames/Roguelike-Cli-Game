from game.core.state import State


class DataView:
    def __init__(self, state: State):
        self._state = state

    def get_phase(self) -> str:
        return str(self._state.phase)
