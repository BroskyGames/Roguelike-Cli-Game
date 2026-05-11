import esper

from game.core.geometry import Pos
from game.core.state import State
from game.ecs.components.data import InRoom


class DataView:
    def __init__(self, state: State):
        self._state = state

    def get_phase(self) -> str:
        return str(self._state.phase)

    def get_player_pos(self) -> tuple[int, int]:
        pos = esper.component_for_entity(self._state.context.player, Pos)
        return pos.x, pos.y

    def debug_print(self) -> str:
        return f"Player Room: {esper.component_for_entity(self._state.context.player, InRoom)}"
