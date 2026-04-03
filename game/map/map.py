from dataclasses import dataclass
from enum import StrEnum

from .layout import Room
from game.core.types import Pos


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

def get_shape(room: Room, display_debug: bool = False) -> dict[Pos, Tile]:
    shape: dict[Pos, Tile] = {}
    for x in range(room.x, room.x + room.width + 1):
        for y in range(room.y, room.y + room.height + 1):
            is_border = x == room.x or y == room.y or x == room.x + room.width or y == room.y + room.height
            # if room.tag == RoomTags.BOSS or room.tag == RoomTags.SPAWN:
            #     raise NotImplementedError()
            shape[Pos(x, y)] = Tile(TileEnum.FLOOR, room.id) if not is_border else Tile(TileEnum.WALL, room.id)
    if display_debug:
        shape[Pos(room.x + room.width // 2 - 1, room.y + room.height // 2)] = Tile(TileEnum.EMPTY, debug=room.tag.value)
        shape[Pos(room.x + room.width // 2, room.y + room.height // 2)] = Tile(TileEnum.EMPTY, debug=str(room.id // 10))
        shape[Pos(room.x + room.width // 2 + 1, room.y + room.height // 2)] = Tile(TileEnum.EMPTY, debug=str(room.id % 10))
    return shape

def build_map(rooms: list[Room]) -> dict[Pos, Tile]:
    game_map = {}
    for room in rooms:
        game_map |= get_shape(room, True)
    return game_map