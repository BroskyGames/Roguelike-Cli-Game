from game.core.geometry import Pos, Size
from game.core.map_types import Tile, TileEnum


class MapView:
    def __init__(self, map_data: dict[Pos, Tile]):
        self.map = map_data

    def get_tile(self, pos: Pos) -> Tile:
        return self.map.get(pos, Tile(TileEnum.EMPTY))

    def get_view(self, off: Pos, size: Size) -> tuple[tuple[Tile, ...], ...]:
        return tuple(
            tuple(
                self.get_tile(Pos(map_x, map_y))
                for map_x in range(off.x, size.width + off.x)
            )
            for map_y in range(off.y, size.height + off.y)
        )
