from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from typing import ClassVar, TYPE_CHECKING

from game.core.geometry import BaseDirections, Directions, Pos, Size
from .graph import RoomNode, bfs
from .special_templates import ROOM_TEMPLATES, accumulate_ascii_doors, ascii_traverser, get_template_size
from ..core.map_types import RoomTypes
from ..utils import Reducer

if TYPE_CHECKING:
    from random import Random


@dataclass(slots=True, frozen=True)
class Door:
    pos: Pos
    belongs_to: int = field(init=False)
    direction: Directions = field(init=False)
    connections: list[Door] = field(default_factory=list, init=False, compare=False, hash=False)

    room: InitVar[Room]

    MAX_CONNECTIONS: ClassVar[int] = 2

    def __post_init__(self, room: Room):
        object.__setattr__(self, 'belongs_to', room.id)
        if self.y == room.y - 1:
            direction = Directions.NORTH
        elif self.x == room.x + room.width:
            direction = Directions.EAST
        elif self.y == room.y + room.height:
            direction = Directions.SOUTH
        elif self.x == room.x - 1:
            direction = Directions.WEST
        else:
            print(self)
            print(room)
            raise AssertionError("Not a valid door position")

        object.__setattr__(self, 'direction', direction)

    def __repr__(self):
        return f"Door(x={self.x}, y={self.y}, room_id={self.belongs_to}, "  # direction={int(self.direction)})

    @property
    def x(self) -> int:
        return self.pos.x

    @property
    def y(self) -> int:
        return self.pos.y

    def can_connect(self) -> bool:
        return len(self.connections) < self.MAX_CONNECTIONS

    def add_connection(self, door: Door):
        if not self.can_connect():
            raise RuntimeError("Door at capacity")

        self.connections.append(door)


# TODO: Implement handling of special rooms: shapes, sizes, finding doors
@dataclass(slots=True)
class Room:
    """Room object that stores the data of ingame room
    [id] = -1 is temporary room used for methods and type safety
    [graph_id] maps to id of RoomNode corresponding to this Room
    [template] is index of ROOM_TEMPLATES[self.type][i]"""
    id: int
    pos: Pos
    size: Size
    type: RoomTypes = RoomTypes.NORMAL
    doors: list[Door] = field(default_factory=list)
    graph_id: int = -1
    template: int | None = None

    def __repr__(self):
        return f"Room(id={self.id}, pos=({self.x}, {self.y}), size=({self.width}, {self.height}), tag='{str(self.type)}', doors={self.doors})"

    @property
    def x(self) -> int:
        return self.pos.x

    @property
    def y(self) -> int:
        return self.pos.y

    @property
    def width(self) -> int:
        return self.size.width

    @property
    def height(self) -> int:
        return self.size.height

    def get_center(self) -> Pos:
        return Pos(self.x + self.width // 2, self.y + self.height // 2)

    def connected_directions(self) -> set[Directions]:
        connected = set()
        for door in self.doors:
            connected.add(door.direction)
        return connected


def compute_door_pos(room: Room) -> tuple[Pos, ...]:
    if room.type == RoomTypes.SPAWN:  # or room.type == RoomTypes.BOSS
        return ascii_traverser(ROOM_TEMPLATES[room.type][room.template], Reducer(accumulate_ascii_doors, ()), room.pos)
    cx, cy = room.get_center()
    return Pos(cx, room.y - 1), Pos(room.x + room.width, cy), Pos(cx, room.y + room.height), Pos(room.x - 1, cy)


def get_available_door_pos(room: Room) -> tuple[Pos, ...]:
    cant_connect_pos = {d.pos for d in room.doors if not d.can_connect()}
    return tuple(pos for pos in compute_door_pos(room) if pos not in cant_connect_pos)


def find_connection_for(a: Room, b: Room) -> tuple[Pos, Pos]:
    min_d = float('inf')
    best_pair = (None, None)

    for x1, y1 in get_available_door_pos(a):
        for x2, y2 in get_available_door_pos(b):
            d = abs(x1 - x2) + abs(y1 - y2)
            if d < min_d:
                min_d = d
                best_pair = (Pos(x1, y1), Pos(x2, y2))

    return best_pair


def find_or_create_door(pos: Pos, room: Room) -> Door:
    for door in room.doors:
        if pos == door.pos:
            return door

    door = Door(pos, room)
    room.doors.append(door)
    return door


def connect_rooms(a: Room, b: Room):
    door_a_pos, door_b_pos = find_connection_for(a, b)
    door_a = find_or_create_door(door_a_pos, a)
    door_b = find_or_create_door(door_b_pos, b)

    door_a.add_connection(door_b)
    door_b.add_connection(door_a)


def rooms_overlap(a: Room, b: Room, padding: int = 1) -> bool:
    return (
            a.x + a.width + padding > b.x and
            a.x < b.x + b.width + padding and
            a.y + a.height + padding > b.y and
            a.y < b.y + b.height + padding
    )


def sample_room_size(node: RoomNode, size_range: tuple[int, int], rng: Random, main_diff: int = 0) -> Size:
    if node.type == RoomTypes.SPAWN:  # or node.type == RoomTypes.BOSS
        return rng.choice(tuple(get_template_size(t) for t in ROOM_TEMPLATES[node.type]))

    w = rng.randint(*size_range)
    h = rng.randint(*size_range)
    if node.type == RoomTypes.MAIN:
        w += main_diff
        h += main_diff
    return Size(w, h)


def find_room_placement(
        size: Size, parent: Room, rooms: list[Room], rng: Random,
        padding_range: tuple[int, int], max_attempts: int, search_radius: int
) -> Pos:
    # noinspection PyShadowingNames
    def try_place_in_direction(direction: Directions) -> Pos | None:
        match direction:
            case Directions.NORTH:
                x = parent.pos.x + rng.randint(-size.width, parent.size.width)
                y = parent.pos.y - size.height - pad
            case Directions.EAST:
                x = parent.pos.x + parent.size.width + pad
                y = parent.pos.y + rng.randint(-size.height, parent.size.height)
            case Directions.SOUTH:
                x = parent.pos.x + rng.randint(-size.width, parent.size.width)
                y = parent.pos.y + parent.size.height + pad
            case Directions.WEST:
                x = parent.pos.x - size.width - pad
                y = parent.pos.y + rng.randint(-size.height, parent.size.height)
            case _:
                raise TypeError(direction)

        position = Pos(x, y)
        if not any([rooms_overlap(Room(-1, position, size), r, pad) for r in rooms]):
            return position

        return None

    def search_nearby(padding_check: int) -> Pos | None:
        parent_center = parent.get_center()

        for dist in range(search_radius + 1):
            for dx in range(-dist, dist + 1):
                dy = dist - abs(dx)

                for sign in (-1, 1) if dy != 0 else (1,):
                    x = parent_center.x + dx
                    y = parent_center.y + sign * dy

                    position = Pos(x, y)

                    if not any(rooms_overlap(Room(-1, position, size), r, padding_check) for r in rooms):
                        return position
        return None

    pad = rng.randint(*padding_range)
    if parent is None:
        return Pos(0, 0)

    for _ in range(max_attempts):
        direction = rng.choice(sorted(BaseDirections - parent.connected_directions()))
        if (pos := try_place_in_direction(direction)) is not None:
            return pos

    if (pos := search_nearby(pad)) is not None:
        return pos

    if (pos := search_nearby(padding_range[0])) is not None:
        return pos

    raise RuntimeError("Failed to place rooms")


def build_rooms_from_graph(
        start: RoomNode, rng: Random,
        size_range: tuple[int, int] = (6, 12), main_diff: int = 2,
        padding_range: tuple[int, int] = (2, 4), max_attempts: int = 5, search_radius: int = 15
) -> list[Room]:
    def place_room(node: RoomNode, rooms: list[Room]) -> list[Room]:
        parent = next(room for room in rooms if node.parent.id == room.graph_id) if node.parent is not None else None

        size = sample_room_size(node, size_range, rng, main_diff)
        pos = find_room_placement(size, parent, rooms, rng, padding_range, max_attempts, search_radius)

        if node.type == RoomTypes.SPAWN:  # or node.type == RoomTypes.BOSS
            template = rng.choice(tuple(
                ROOM_TEMPLATES[node.type].index(t) for t in ROOM_TEMPLATES[node.type] if get_template_size(t) == size))

            room = Room(
                id=len(rooms),
                type=node.type,
                pos=pos,
                size=size,
                graph_id=node.id,
                template=template
            )
        else:
            room = Room(
                id=len(rooms),
                type=node.type,
                pos=pos,
                size=size,
                graph_id=node.id
            )

        rooms.append(room)

        if parent:
            connect_rooms(room, parent)

        return rooms

    return bfs(start, Reducer(place_room, []))
