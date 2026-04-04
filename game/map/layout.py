from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING
from ..utils import Reducer
from .graph import RoomNode, bfs
from game.core.core_types import Directions, DirectionsEnum, Pos, Size
from .room_tags import RoomTags
if TYPE_CHECKING:
    from random import Random

class RoomPlacementError(Exception):
    """Raised when a room cannot be placed on the map."""
    pass

@dataclass(slots=True, frozen=True)
class Door:
    pos: Pos
    belongs_to: int = field(init=False)
    direction: DirectionsEnum = field(init=False)

    room: InitVar["Room"]

    def __post_init__(self, room: "Room"):
        object.__setattr__(self, 'belongs_to', room.id)
        if self.y == room.y - 1:
            direction = DirectionsEnum.NORTH
        elif self.x == room.x + room.width:
            direction = DirectionsEnum.EAST
        elif self.y == room.y + room.height:
            direction = DirectionsEnum.SOUTH
        elif self.x == room.x - 1:
            direction = DirectionsEnum.WEST
        else:
            raise "Not a valid door position"

        object.__setattr__(self, 'direction', direction)

    def __repr__(self):
        return f"Door(x={self.x}, y={self.y}, room_id={self.belongs_to}, direction={int(self.direction)})"

    @property
    def x(self) -> int:
        return self.pos.x

    @property
    def y(self) -> int:
        return self.pos.y

# TODO: Implement handling of special rooms: shapes, sizes, unused_doors
@dataclass(slots=True)
class Room:
    """Room object that stores the data of ingame room
    [id] = -1 is temporary room used for methods and type safety
    [graph_id] maps to id of RoomNode corresponding to this Room
    [doors] and [connections] are aligned"""
    id: int
    pos: Pos
    size: Size
    tag: RoomTags = RoomTags.NORMAL
    doors: list[Door] = field(default_factory=list)
    connections: list[int] = field(default_factory=list)
    graph_id: int = -1

    def __repr__(self):
        return f"Room(id={self.id}, pos=({self.x}, {self.y}), size=({self.width}, {self.height}), tag='{str(self.tag)}', connections={self.connections}, doors={self.doors})"

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

    def connected_directions(self) -> set[DirectionsEnum]:
        connected = set()
        for door in self.doors:
            connected.add(door.direction)
        return connected

def compute_unused_doors_pos(room: Room) -> set[Pos]:
    # if room.tag == RoomTags.BOSS or room.tag == RoomTags.SPAWN:
        # raise NotImplementedError()
    cx, cy = room.get_center()
    return {Pos(cx, room.y - 1), Pos(room.x + room.width, cy), Pos(cx, room.y + room.height), Pos(room.x - 1, cy)} - {door.pos for door in room.doors}

def find_connection_for(a: Room, b: Room) -> tuple[Pos, Pos]:
    min_d = float('inf')
    best_pair = (None, None)

    for x1, y1 in compute_unused_doors_pos(a):
        for x2, y2 in compute_unused_doors_pos(b):
            d = abs(x1 - x2) + abs(y1 - y2)
            if d < min_d:
                min_d = d
                best_pair = (Pos(x1, y1), Pos(x2, y2))

    return best_pair

def connect_rooms(a: Room, b: Room):
    door_a_pos, door_b_pos = find_connection_for(a, b)

    a.connections.append(b.id)
    a.doors.append(Door(door_a_pos, a))
    b.connections.append(a.id)
    b.doors.append(Door(door_b_pos, b))

def rooms_overlap(a: Room, b: Room, padding: int = 1) -> bool:
    return (
            a.x + a.width + padding > b.x and
            a.x < b.x + b.width + padding and
            a.y + a.height + padding > b.y and
            a.y < b.y + b.height + padding
    )

def sample_room_size(node: RoomNode, size_range: tuple[int, int], rng: "Random", main_diff: int = 0) -> Size:
    # if node.tag == RoomTags.BOSS or node.tag == RoomTags.SPAWN:
    #     raise NotImplementedError()

    w = rng.randint(*size_range)
    h = rng.randint(*size_range)
    if node.tag == RoomTags.MAIN:
        w += main_diff
        h += main_diff
    return Size(w, h)

def find_room_placement(
        size: Size, parent: Room, rooms: list[Room], rng: "Random",
        padding_range: tuple[int, int], max_attempts: int, search_radius: int
) -> Pos:
    # noinspection PyShadowingNames
    def try_place_in_direction(direction: DirectionsEnum) -> Pos | None:
        match direction:
            case DirectionsEnum.NORTH:
                x = parent.pos.x + rng.randint(-size.width, parent.size.width)
                y = parent.pos.y - size.height - pad
            case DirectionsEnum.EAST:
                x = parent.pos.x + parent.size.width + pad
                y = parent.pos.y + rng.randint(-size.height, parent.size.height)
            case DirectionsEnum.SOUTH:
                x = parent.pos.x + rng.randint(-size.width, parent.size.width)
                y = parent.pos.y + parent.size.height + pad
            case DirectionsEnum.WEST:
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
        direction = rng.choice(tuple(Directions - parent.connected_directions()))
        if (pos := try_place_in_direction(direction)) is not None:
            return pos

    if (pos := search_nearby(pad)) is not None:
        return pos

    if (pos := search_nearby(padding_range[0])) is not None:
        return pos

    raise RoomPlacementError()

def build_rooms_from_graph(
        start: RoomNode, rng: "Random",
        size_range: tuple[int, int] = (6, 12), main_diff: int = 2,
        padding_range: tuple[int, int] = (2, 4), max_attempts: int = 5, search_radius: int = 15
) -> list[Room]:
    def place_room(node: RoomNode, rooms: list[Room]) -> list[Room]:
        parent = next(room for room in rooms if node.parent.id == room.graph_id) if node.parent is not None else None

        size = sample_room_size(node, size_range, rng, main_diff)
        pos = find_room_placement(size, parent, rooms, rng, padding_range, max_attempts, search_radius)

        room = Room(
            id=len(rooms),
            tag=node.tag,
            pos=pos,
            size=size,
            graph_id=node.id
        )
        rooms.append(room)

        if parent:
            connect_rooms(room, parent)

        return rooms

    return bfs(start, Reducer(place_room, []))