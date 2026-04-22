import esper

from game.core.geometry import Pos
from game.core.map_types import Tile, TileType
from game.core.state import State
from game.domain.components import Display, InRoom, Visible
from game.ui.rect import Rect


class MapView:
    def __init__(self, state: State):
        self._state = state

        room = esper.component_for_entity(self._state.player, InRoom).room
        assert room is not None, "Player not in room on spawn"
        self._cam = self._state.rooms[room].get_center()

    def get_tile(self, y: int, x: int) -> str:
        entities = {
            pos: ent.char
            for _, (ent, pos, _) in esper.get_components(Display, Pos, Visible)
        }

        return entities.get(Pos(x, y)) or str(self._state.map.get(Pos(x, y), Tile(TileType.EMPTY)))

    def get_view(self, rect: Rect) -> tuple[tuple[str, ...], ...]:
        return tuple(
            tuple(
                self.get_tile(map_y, map_x)
                for map_x in range(rect.x, rect.w + rect.x)
            )
            for map_y in range(rect.y, rect.h + rect.y)
        )

    def get_camera(self) -> tuple[int, int]:
        room = esper.component_for_entity(self._state.player, InRoom).room
        if room is not None:
            self._cam = self._state.rooms[room].get_center()

        return self._cam[1], self._cam[0]
