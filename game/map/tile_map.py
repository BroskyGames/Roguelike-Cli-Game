from collections import defaultdict
from functools import partial
from typing import cast

from game.core.geometry import Pos
from game.domain.directions import DIRECTION_VECTORS, Directions, DirectionsDiagonals
from game.domain.map_types import RoomTypes, Tile, TileType
from game.utils import Reducer, combine_reducers

from .corridor import Corridor
from .room import Room
from .special_templates import ROOM_TEMPLATES, acc_ascii_doors, ascii_traverser


def build_map(
    rooms: tuple[Room, ...], corridors: list[Corridor], overlay: bool = False
) -> dict[Pos, Tile]:
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
        template = ROOM_TEMPLATES[room.type][cast(int, room.template)]

        _, doors = ascii_traverser(
            template,
            combine_reducers(
                Reducer(write_room_shape, shape),
                Reducer(acc_ascii_doors, []),
            ),
        )

        for ascii_door in doors:
            if not any(ascii_door == door.pos for door in room.doors):
                shape[ascii_door] = Tile(TileType.WALL, room.id)
    else:
        room_x, room_y = room.pos
        room_w, room_h = room.size
        for x in range(room_x - 1, room_x + room_w + 1):
            for y in range(room_y - 1, room_y + room_h + 1):
                pos = Pos(x, y)

                is_border = (
                    (x == room_x - 1)
                    or (y == room_y - 1)
                    or (x == room_x + room_w)
                    or (y == room_y + room_h)
                )

                if not is_border:
                    shape[pos] = Tile(TileType.FLOOR, room.id)
                    continue

                if any(pos == door.pos for door in room.doors):
                    shape[pos] = Tile(TileType.DOOR, room.id)
                    continue

                shape[pos] = Tile(TileType.WALL, room.id)

    if overlay:
        center = room.center

        shape[center + DIRECTION_VECTORS[Directions.WEST]].debug = room.type.value
        shape[center].debug = str(room.id // 10)
        shape[center + DIRECTION_VECTORS[Directions.EAST]].debug = str(room.id % 10)

        shape[Pos(0, 0)].debug = "+"

    return shape


def _get_corridor_shape(corridor: Corridor) -> dict[Pos, Tile]:
    shape = {pos: Tile(TileType.FLOOR) for pos in corridor.path}
    doors = {d.pos for d in corridor.connects}

    for pos in corridor.path:
        for direction in DirectionsDiagonals:
            neighbor = pos + DIRECTION_VECTORS[direction]
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
        TileType.EMPTY: 0,
    }
    return new if priority[new.type] >= priority[base.type] else base


def _acc_ascii_shape(
    data: tuple[Pos, str], acc: dict[Pos, Tile], room_id: int
) -> dict[Pos, Tile]:
    pos, char = data
    match char:
        case ".":
            acc[pos] = Tile(TileType.FLOOR, room_id)
        case "#":
            acc[pos] = Tile(TileType.WALL, room_id)
        case "D":
            acc[pos] = Tile(TileType.DOOR, room_id)
    return acc
