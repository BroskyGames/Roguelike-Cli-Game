from dataclasses import dataclass, field
from enum import StrEnum


class TileType(StrEnum):
    EMPTY = ' '
    FLOOR = '.'
    DOOR = 'D'
    WALL = '#'


WALKABLE_TYPES = {
    TileType.EMPTY: True,
    TileType.FLOOR: True,
    TileType.DOOR: True,
    TileType.WALL: False,
}


@dataclass(slots=True)
class Tile:
    type: TileType = TileType.EMPTY
    room_id: int = -1
    debug: str = ''
    walkable: bool = field(init=False)
    transparent: bool = field(init=False)

    def __post_init__(self):
        self.walkable = WALKABLE_TYPES[self.type]
        self.transparent = self.walkable if self.type is not TileType.DOOR else False

    def __str__(self):
        return self.debug if self.debug else str(self.type)


class RoomTypes(StrEnum):
    NORMAL = 'N'
    SPAWN = 'S'
    MAIN = 'M'
    BOSS = 'B'
    GENETIC = 'G'
    TRAP = 'T'
    # SHOP
