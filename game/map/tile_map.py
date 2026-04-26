from collections import defaultdict
from functools import partial

from game.core.geometry import Directions, DirectionsDiagonals, Pos
from game.core.map_types import RoomTypes, Tile, TileType
from game.utils import Reducer, combine_reducers
from .corridor import Corridor
from .room import Room
from .special_templates import ROOM_TEMPLATES, acc_ascii_doors, ascii_traverser


def build_map(rooms: tuple[Room, ...], corridors: list[Corridor], overlay: bool = False) -> defaultdict[Pos, Tile]:
    game_map = defaultdict(lambda: Tile())
    for room in rooms:
        for pos, tile in _get_room_shape(room, overlay).items():
            game_map[pos] = _merge_tile(game_map[pos], tile)
    for corridor in corridors:
        for pos, tile in _get_corridor_shape(corridor).items():
            game_map[pos] = _merge_tile(game_map[pos], tile)
    return game_map


def _get_room_shape(room: Room, overlay: bool = False) -> dict[Pos, Tile]:
    shape: defaultdict[Pos, Tile] = defaultdict(lambda: Tile())

    if room.type == RoomTypes.SPAWN:  # or room.type == RoomTags.BOSS
        write_room_shape = partial(_acc_ascii_shape, room_id=room.id)
        template = ROOM_TEMPLATES[room.type][room.template]

        _, doors = ascii_traverser(
            template,
            combine_reducers(
                Reducer(write_room_shape, shape),
                Reducer(acc_ascii_doors, []),
            )
        )

        for ascii_door in doors:
            if not any(ascii_door == door.pos for door in room.doors):
                shape[ascii_door] = Tile(TileType.WALL, room.id)
    else:
        for x in range(room.x - 1, room.x + room.width + 1):
            for y in range(room.y - 1, room.y + room.height + 1):
                pos = Pos(x, y)

                is_border = (
                        (x == room.x - 1) or
                        (y == room.y - 1) or
                        (x == room.x + room.width) or
                        (y == room.y + room.height)
                )

                if not is_border:
                    shape[pos] = Tile(TileType.FLOOR, room.id)
                    continue

                if any(pos == door.pos for door in room.doors):
                    shape[pos] = Tile(TileType.DOOR, room.id)
                    continue

                shape[pos] = Tile(TileType.WALL, room.id)

    if overlay:
        center = room.get_center()

        shape[center + Directions.WEST.vector()].debug = room.type.value
        shape[center].debug = str(room.id // 10)
        shape[center + Directions.EAST.vector()].debug = str(room.id % 10)

        shape[Pos(0, 0)].debug = '+'

    return shape


def _get_corridor_shape(corridor: Corridor) -> dict[Pos, Tile]:
    shape = {pos: Tile(TileType.FLOOR) for pos in corridor.path}
    doors = {d.pos for d in corridor.connects}

    for pos in corridor.path:
        for direction in DirectionsDiagonals:
            neighbor = pos + direction.vector()
            if neighbor in doors:
                continue
            if neighbor in shape:
                continue
            shape[neighbor] = Tile(TileType.WALL)

    return shape


def _merge_tile(base: Tile, new: Tile) -> Tile:
    priority = {
        TileType.DOOR: 3,
        TileType.FLOOR: 2,
        TileType.WALL: 1,
        TileType.EMPTY: 0
    }
    return new if priority[new.type] >= priority[base.type] else base


def _acc_ascii_shape(data: tuple[Pos, str], acc: dict[Pos, Tile], room_id: int) -> dict[Pos, Tile]:
    pos, char = data
    match char:
        case '.':
            acc[pos] = Tile(TileType.FLOOR, room_id)
        case '#':
            acc[pos] = Tile(TileType.WALL, room_id)
        case 'D':
            acc[pos] = Tile(TileType.DOOR, room_id)
    return acc
