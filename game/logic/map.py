from dataclasses import dataclass, field
from typing import Self

from .graph import RoomNode, RoomTags
from ..utils import Pos, Size, get_rng, init_rng


@dataclass
class Room:
    id: int
    pos: Pos
    size: Size
    tag: RoomTags = RoomTags.NORMAL
    _possible_doors: list[Pos] = field(default_factory=list)
    doors: list[Pos] = field(default_factory=list)
    connections: list[Self] = field(default_factory=list)

    def center(self) -> Pos:
        return Pos(self.pos.x + self.size.width // 2, self.pos.y + self.size.height // 2)

    def add_connection(self, other: Self, door: int):
        self.connections.append(other)
        self.doors.append(self._possible_doors.pop(door))

    def nearest_doors(self, other: Self) -> tuple[int, int]:
        min_d = float('inf')
        best_pair = (None, None)

        for i, (x1, y1) in enumerate(self._possible_doors):
            for j, (x2, y2) in enumerate(other._possible_doors):
                d = abs(x1 - x2) + abs(y1 - y2)
                if d < min_d:
                    min_d = d
                    best_pair = (i, j)

        return best_pair

    def if_overlap(self, other: Self, padding: int = 1) -> bool:
        return (
                self.pos.x + self.size.width + padding > other.pos.x and
                self.pos.x < other.pos.x + other.size.width + padding and
                self.pos.y + self.size.height + padding > other.pos.y and
                self.pos.y < other.pos.y + other.size.height + padding
        )


def get_room_size(node: RoomNode, min_max_size: range, main_diff: int) -> Size:
    if node.tag == RoomTags.BOSS or node.tag == RoomTags.SPAWN:
        raise NotImplementedError()

    w, h = get_rng().choices(min_max_size, k=2)
    if node.tag == RoomTags.MAIN:
        w += main_diff
        h += main_diff
    return Size(w, h)

def get_room_pos(size: Size, parent: Room, padding: range, rooms: list[Room], max_attempts: int = 5, search_radius: int = 10) -> Pos:
    pad = get_rng().choice(padding)
    if parent is None:
        return Pos(0, 0)

    for _ in range(max_attempts):
        direction = get_rng().choice(range(4))
        match direction:
            case 0:
                x = parent.pos.x + get_rng().randint(-size.width, parent.size.width + size.width)
                y = parent.pos.y - size.height - pad
            case 1:
                x = parent.pos.x + parent.size.width + pad
                y = parent.pos.y + get_rng().randint(-size.height, parent.size.height + size.height)
            case 2:
                x = parent.pos.x + get_rng().randint(-size.width, parent.size.width + size.width)
                y = parent.pos.y + parent.size.height + pad
            case 3:
                x = parent.pos.x - size.width - pad
                y = parent.pos.y + get_rng().randint(-size.height, parent.size.height + size.height)
            case _:
                raise AssertionError('Unhandled case')

        # pos = Pos(x, y)
        # if not rooms_overlap(pos, size, existing_rooms, padding=pad):
        #     return pos

    # parent_center = parent.center()
    # for dx in range(-search_radius, search_radius + 1):
    #     for dy in range(-search_radius, search_radius + 1):
    #         pos = Pos(parent_center.x + dx, parent_center.y + dy)
    #         if not rooms_overlap(pos, size, existing_rooms, padding=pad):
    #             return pos
    #
    # return pos


def create_rooms_from_graph(spawn_node: RoomNode, min_max_size: range = range(6,13), main_diff: int = 2, padding: range = range(2, 5)) -> dict[int, Room]:
    rooms = {}

    def place_room(node: RoomNode, parent: Room = None, depth=0):
        size = get_room_size(node, min_max_size, main_diff)
        pos = get_room_pos(size, parent, padding, list(rooms.values()))

        room = Room(
            id=node.id,
            tag=node.tag,
            pos=pos,
            size=size
        )
        rooms[node.id] = room

        if parent:
            # TODO: Implement a real corridor connection
            door, parent_door = room.nearest_doors(parent)
            parent.add_connection(room, parent_door)
            room.add_connection(parent, door)

        for child in node.children:
            place_room(child, room, depth + 1)

    place_room(spawn_node)
    return rooms