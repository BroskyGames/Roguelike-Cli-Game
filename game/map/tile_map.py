from collections import defaultdict

from .corridor import Corridor
from .layout import Room
from .special_templates import ROOM_TEMPLATES, ascii_traverser
from ..core.geometry import BaseDirections, Directions, Pos
from ..core.map_types import RoomTypes, Tile, TileType
from ..utils import Reducer


def _merge_tile(base: Tile, new: Tile) -> Tile:
    priority = {
        TileType.DOOR: 3,
        TileType.FLOOR: 2,
        TileType.WALL: 1,
        TileType.EMPTY: 0
    }
    return new if priority[new.type] >= priority[base.type] else base


def _get_room_shape(room: Room, overlay: bool = False) -> dict[Pos, Tile]:
    def accumulate_ascii_shape(data: tuple[Pos, str], acc: dict[Pos, Tile]) -> dict[Pos, Tile]:
        pos, char = data
        match char:
            case '.':
                acc[pos] = Tile(TileType.FLOOR, room.id)
            case '#':
                acc[pos] = Tile(TileType.WALL, room.id)
            case 'D':
                acc[pos] = Tile(TileType.DOOR, room.id)
        return acc

    def add_overlay():
        center = room.get_center()

        shape[center + Directions.WEST.vector()].debug = room.type.value
        shape[center].debug = str(room.id // 10)
        shape[center + Directions.EAST.vector()].debug = str(room.id % 10)

        shape[Pos(0, 0)].debug = '+'

    shape: defaultdict[Pos, Tile] = defaultdict(lambda: Tile(TileType.EMPTY))

    for x in range(room.x - 1, room.x + room.width + 1):
        for y in range(room.y - 1, room.y + room.height + 1):
            if room.type == RoomTypes.SPAWN:  # or room.type == RoomTags.BOSS
                shape = ascii_traverser(ROOM_TEMPLATES[room.type][room.template], Reducer(accumulate_ascii_shape, {}))
            else:
                is_border = (x == room.x - 1) or (y == room.y - 1) or (x == room.x + room.width) or (
                        y == room.y + room.height)

                shape[Pos(x, y)] = Tile(TileType.FLOOR, room.id) if not is_border else \
                    Tile(TileType.DOOR, room.id) if any(Pos(x, y) == door.pos for door in room.doors) else \
                        Tile(TileType.WALL, room.id)

    if overlay:
        add_overlay()

    return shape


def _get_corridor_shape(corridor: Corridor) -> dict[Pos, Tile]:
    shape = {pos: Tile(TileType.FLOOR) for pos in corridor.path}
    doors = {d.pos for d in corridor.connects}

    for pos in corridor.path:
        for direction in BaseDirections:
            neighbor = pos + direction.vector()
            if neighbor in doors:
                continue
            if neighbor in shape:
                continue
            shape[neighbor] = Tile(TileType.WALL)

    return shape


def build_map(rooms: tuple[Room, ...], corridors: list[Corridor], overlay: bool = False) -> defaultdict[Pos, Tile]:
    game_map = defaultdict(lambda: Tile(TileType.EMPTY))
    for room in rooms:
        for pos, tile in _get_room_shape(room, overlay).items():
            game_map[pos] = _merge_tile(game_map[pos], tile)
    for corridor in corridors:
        for pos, tile in _get_corridor_shape(corridor).items():
            game_map[pos] = _merge_tile(game_map[pos], tile)
    return game_map
