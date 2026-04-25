import esper

from game.core.context import Context
from game.core.geometry import Pos
from game.core.map_types import Tile, TileType
from game.domain.components.data import Display, InRoom
from game.ui.rect import Rect


class MapView:
    def __init__(self, context: Context):
        self._context = context

        room = esper.component_for_entity(self._context.player, InRoom).room
        assert room is not None, "Player not in room on spawn"
        self._cam = self._context.rooms[room].get_center()

    def get_tile(self, y: int, x: int) -> str:
        pos = Pos(x, y)

        best = None

        for ent in self._context.entities_index.get(pos, ()):
            disp = esper.try_component(ent, Display)
            if disp and (not best or disp.priority > best.priority):
                best = disp

        if best:
            return best.char

        return str(self._context.map.get(pos, Tile(TileType.EMPTY)))

    def get_view(self, rect: Rect) -> tuple[tuple[str, ...], ...]:
        return tuple(
            tuple(
                self.get_tile(map_y, map_x)
                for map_x in range(rect.x, rect.w + rect.x)
            )
            for map_y in range(rect.y, rect.h + rect.y)
        )

    def get_camera(self) -> tuple[int, int]:
        room = esper.component_for_entity(self._context.player, InRoom).room
        if room is not None:
            self._cam = self._context.rooms[room].get_center()

        return self._cam[1], self._cam[0]
