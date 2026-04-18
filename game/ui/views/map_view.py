from game.core.geometry import Pos
from game.core.map_types import Tile, TileEnum
from game.core.state import State
from game.ui.rect import Rect


class MapView:
    def __init__(self, state: State):
        self._state = state

    def get_tile(self, y: int, x: int) -> Tile:
        return self._state.map.get(Pos(x, y), Tile(TileEnum.EMPTY))

    def get_view(self, rect: Rect) -> tuple[tuple[Tile, ...], ...]:
        return tuple(
            tuple(
                self.get_tile(map_y, map_x)
                for map_x in range(rect.x, rect.w + rect.x)
            )
            for map_y in range(rect.y, rect.h + rect.y)
        )

    def get_camera(self) -> tuple[int, int]:
        pos: Pos = self._state.rooms[self._state.last_room].get_center()
        return pos.y, pos.x
