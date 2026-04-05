from dataclasses import dataclass
from enum import StrEnum

from .corridor import Corridor
from .layout import Room
from .room_types import RoomTypes
from ..core.core_types import Pos
from .special_templates import ROOM_TEMPLATES, ascii_traverser
from ..utils import Reducer


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


def get_room_shape(room: Room, display_debug: bool = False) -> dict[Pos, Tile]:
    def accumulate_ascii_shape(data: tuple[Pos, str], acc: dict[Pos, Tile]) -> dict[Pos, Tile]:
        pos, char = data
        acc |= {
            pos: Tile(TileEnum.FLOOR, room.id) if char == '.' else
            Tile(TileEnum.WALL, room.id) if char == '#' else
            Tile(TileEnum.EMPTY) if char == ' ' else
            Tile(TileEnum.DOOR)
        }
        return acc

    shape: dict[Pos, Tile] = {}

    for x in range(room.x - 1, room.x + room.width + 1):
        for y in range(room.y - 1, room.y + room.height + 1):
            if room.type == RoomTypes.SPAWN: # or room.type == RoomTags.BOSS
                shape = ascii_traverser(ROOM_TEMPLATES[room.type][room.template], Reducer(accumulate_ascii_shape, {}))
            else:
                is_border = (x == room.x - 1) or (y == room.y - 1) or (x == room.x + room.width) or (y == room.y + room.height)

                shape[Pos(x, y)] = Tile(TileEnum.FLOOR, room.id) if not is_border else \
                    Tile(TileEnum.DOOR, room.id) if any(Pos(x, y) == door.pos for door in room.doors) else \
                        Tile(TileEnum.WALL, room.id)

    if display_debug:
        shape[Pos(room.x + room.width // 2 - 1, room.y + room.height // 2)] = Tile(TileEnum.EMPTY, debug=room.type.value)
        shape[Pos(room.x + room.width // 2, room.y + room.height // 2)] = Tile(TileEnum.EMPTY, debug=str(room.id // 10))
        shape[Pos(room.x + room.width // 2 + 1, room.y + room.height // 2)] = Tile(TileEnum.EMPTY, debug=str(room.id % 10))

    return shape

def get_corridor_shape(corridor: Corridor) -> dict[Pos, Tile]:
    return {pos: Tile(TileEnum.FLOOR) for pos in corridor.path}

def build_map(rooms: list[Room], corridors: list[Corridor]) -> dict[Pos, Tile]:
    game_map = {}
    for room in rooms:
        game_map |= get_room_shape(room, True)
    for corridor in corridors:
        game_map |= get_corridor_shape(corridor)
    return game_map