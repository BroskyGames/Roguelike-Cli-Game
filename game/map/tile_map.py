from .corridor import Corridor
from .layout import Room
from .special_templates import ROOM_TEMPLATES, ascii_traverser
from ..core.geometry import BaseDirections, Pos
from ..core.map_types import RoomTypes, Tile, TileEnum
from ..utils import Reducer


def merge_tile(base: Tile, new: Tile) -> Tile:
    priority = {
        TileEnum.DOOR: 3,
        TileEnum.FLOOR: 2,
        TileEnum.WALL: 1,
        TileEnum.EMPTY: 0
    }
    return new if priority[new.kind] >= priority[base.kind] else base


def get_room_shape(room: Room, display_debug: bool = False) -> dict[Pos, Tile]:
    def accumulate_ascii_shape(data: tuple[Pos, str], acc: dict[Pos, Tile]) -> dict[Pos, Tile]:
        pos, char = data
        match char:
            case '.':
                acc[pos] = Tile(TileEnum.FLOOR, room.id)
            case '#':
                acc[pos] = Tile(TileEnum.WALL, room.id)
            case 'D':
                acc[pos] = Tile(TileEnum.DOOR, room.id)
        return acc

    shape: dict[Pos, Tile] = {}

    for x in range(room.x - 1, room.x + room.width + 1):
        for y in range(room.y - 1, room.y + room.height + 1):
            if room.type == RoomTypes.SPAWN:  # or room.type == RoomTags.BOSS
                shape = ascii_traverser(ROOM_TEMPLATES[room.type][room.template], Reducer(accumulate_ascii_shape, {}))
            else:
                is_border = (x == room.x - 1) or (y == room.y - 1) or (x == room.x + room.width) or (
                        y == room.y + room.height)

                shape[Pos(x, y)] = Tile(TileEnum.FLOOR, room.id) if not is_border else \
                    Tile(TileEnum.DOOR, room.id) if any(Pos(x, y) == door.pos for door in room.doors) else \
                        Tile(TileEnum.WALL, room.id)

    if display_debug:
        shape[Pos(room.x + room.width // 2 - 1, room.y + room.height // 2)] = Tile(TileEnum.FLOOR,
                                                                                   debug=room.type.value)
        shape[Pos(room.x + room.width // 2, room.y + room.height // 2)] = Tile(TileEnum.FLOOR, debug=str(room.id // 10))
        shape[Pos(room.x + room.width // 2 + 1, room.y + room.height // 2)] = Tile(TileEnum.FLOOR,
                                                                                   debug=str(room.id % 10))
        shape[Pos(0, 0)] = Tile(shape[Pos(0, 0)].kind if shape.get(Pos(0, 0)) is not None else TileEnum.EMPTY,
                                debug='+')

    return shape


def get_corridor_shape(corridor: Corridor) -> dict[Pos, Tile]:
    shape = {pos: Tile(TileEnum.FLOOR) for pos in corridor.path}
    doors = {d.pos for d in corridor.connects}

    for pos in corridor.path:
        for direction in BaseDirections:
            neighbor = pos + direction.vector()
            if neighbor in doors:
                continue
            if neighbor in shape:
                continue
            shape[neighbor] = Tile(TileEnum.WALL)

    return shape


def build_map(rooms: list[Room], corridors: list[Corridor]) -> dict[Pos, Tile]:
    game_map = {}
    for room in rooms:
        for pos, tile in get_room_shape(room, True).items():
            game_map[pos] = merge_tile(game_map.get(pos, Tile(TileEnum.EMPTY)), tile)
    for corridor in corridors:
        for pos, tile in get_corridor_shape(corridor).items():
            game_map[pos] = merge_tile(game_map.get(pos, Tile(TileEnum.EMPTY)), tile)
    return game_map
