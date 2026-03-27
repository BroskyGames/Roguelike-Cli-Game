from dataclasses import dataclass, field
from typing import Self

from .graph import RoomNode, RoomTags
from ..utils import Pos, Size, get_rng, init_rng


@dataclass
class Room:
    id: int
    x: int
    y: int
    width: int
    height: int
    tag: RoomTags = RoomTags.NORMAL
    doors: list[Pos] = field(default_factory=list)
    connections: list[Self] = field(default_factory=list)

    def center(self) -> Pos:
        return self.x + self.width // 2, self.y + self.height // 2

    def add_connection(self, other: Self, door_pos: tuple[int, int]):
        self.connections.append(other)
        self.doors.append(door_pos)

    def nearest_doors(self, other: Self) -> Pos:
        min_d = float('inf')
        best_pair = (None, None)

        for i, (x1, y1) in enumerate(self.doors):
            for j, (x2, y2) in enumerate(other.doors):
                d = abs(x1 - x2) + abs(y1 - y2)
                if d < min_d:
                    min_d = d
                    best_pair = (i, j)

        return best_pair

def get_room_size(node: RoomNode, min_size=6, max_size=12, main_diff=2) -> Size:
    if node.tag == RoomTags.BOSS or node.tag == RoomTags.SPAWN:
        raise NotImplementedError()

    w, h = get_rng().randint(min_size, max_size), get_rng().randint(min_size, max_size)
    if node.tag == RoomTags.MAIN:
        w += main_diff
        h += main_diff
    return w, h

def create_rooms_from_graph(spawn_node: RoomNode, min_size=6, max_size=12, main_diff=2,  spacing=2) -> dict[int, Room]:
    rooms = {}

    def place_room(node: RoomNode, parent_room: Room = None, depth=0):
        rng = get_rng()

        width, height = get_room_size(node, min_size, max_size, main_diff)

        if parent_room is None:
            x, y = 40, 20
        else:
            px, py = parent_room.center()
            x = px + rng.randint(parent_room.width // 2 + spacing, parent_room.width + spacing + width)
            y = py + rng.randint(-height // 2, height // 2)

        room = Room(
            id=node.id,
            tag=node.tag,
            x=x,
            y=y,
            width=width,
            height=height
        )
        rooms[node.id] = room

        if parent_room:
            door, parent_door = room.nearest_doors(parent_room)
            parent_room.add_connection(room, parent_room.doors[parent_door])
            room.add_connection(parent_room, room.doors[door])

        for child in node.children:
            place_room(child, room, depth + 1)

    place_room(spawn_node)
    return rooms