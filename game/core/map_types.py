from dataclasses import dataclass
from enum import StrEnum


class TileEnum(StrEnum):
    EMPTY = ' '
    FLOOR = '.'
    WALL = '#'
    DOOR = 'D'


@dataclass(slots=True)
class Tile:
    kind: TileEnum
    room_id: int = -1
    debug: str = ''

    def __str__(self):
        return self.debug if self.debug else str(self.kind)


class RoomTypes(StrEnum):
    NORMAL = 'N'
    SPAWN = 'S'
    MAIN = 'M'
    BOSS = 'B'
    GENETIC = 'G'
    TRAP = 'T'
    # SHOP
