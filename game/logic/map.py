from dataclasses import dataclass, field

from .graph import RoomNode, RoomTags
from ..utils import Directions, DirectionsEnum, Pos, Size, get_rng

# TODO: Implement handling of special rooms: shapes, sizes, unused_doors
@dataclass(slots=True)
class Room:
    """Room object that stores the data of ingame room
    [id] = -1 is temporary room used for methods and type safety"""
    id: int
    pos: Pos
    size: Size
    tag: RoomTags = RoomTags.NORMAL
    unused_doors: list[Pos] = field(default_factory=list)
    doors: list[Pos] = field(default_factory=list)
    connections: list["Room"] = field(default_factory=list)

    def __post_init__(self):
        if id != -1:
            self._find_unused_doors()

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

    def get_shape(self) -> dict[Pos, str]:
        shape = {}
        for x in range(self.x, self.x + self.width + 1):
            for y in range(self.y, self.y + self.height + 1):
                 # if self.tag == RoomTags.BOSS or self.tag == RoomTags.SPAWN:
                 #     raise NotImplementedError()
                shape[Pos(x, y)] = '#' if x == self.x or y == self.y or x == self.x + self.width or y == self.y + self.height else '.'
        shape[Pos(self.x + self.width // 2-1, self.y + self.height // 2)] = self.tag.value
        shape[Pos(self.x + self.width // 2, self.y + self.height // 2)] = str(self.id // 10)
        shape[Pos(self.x + self.width // 2+1, self.y + self.height // 2)] = str(self.id % 10)
        return shape

    def _find_unused_doors(self):
        # if self.tag == RoomTags.BOSS or self.tag == RoomTags.SPAWN:
            # raise NotImplementedError()
        cx, cy = self.get_center()
        self.unused_doors = [Pos(cx, self.y), Pos(self.x+self.width, cy), Pos(cx, self.y+self.height), Pos(self.x, cy)]

    def add_connection(self, other: "Room", door: int):
        self.connections.append(other)
        self.doors.append(self.unused_doors.pop(door))

    def connected_directions(self) -> set[DirectionsEnum]:
        connected = set()
        for door in self.doors:
            if door.y == self.y:
                connected.add(DirectionsEnum.NORTH)
            if door.x == self.x + self.width:
                connected.add(DirectionsEnum.EAST)
            if door.y == self.y + self.height:
                connected.add(DirectionsEnum.SOUTH)
            if door.x == self.x:
                connected.add(DirectionsEnum.WEST)
        return connected

    def nearest_doors_indexes(self, other: "Room") -> tuple[int, int]:
        min_d = float('inf')
        best_pair = (None, None)

        for i, (x1, y1) in enumerate(self.unused_doors):
            for j, (x2, y2) in enumerate(other.unused_doors):
                d = abs(x1 - x2) + abs(y1 - y2)
                if d < min_d:
                    min_d = d
                    best_pair = (i, j)

        return best_pair

    def overlaps(self, other: "Room", padding: int = 1) -> bool:
        return (
                self.x + self.width + padding > other.x and
                self.x < other.x + other.width + padding and
                self.y + self.height + padding > other.y and
                self.y < other.y + other.height + padding
        )

def generate_room_size(node: RoomNode, min_max_size: range, main_diff: int) -> Size:
    # if node.tag == RoomTags.BOSS or node.tag == RoomTags.SPAWN:
    #     raise NotImplementedError()

    w, h = get_rng().choices(min_max_size, k=2)
    if node.tag == RoomTags.MAIN:
        w += main_diff
        h += main_diff
    return Size(w, h)

def find_room_pos(size: Size, parent: Room, padding: range, rooms: list[Room], max_attempts: int = 5, search_radius: int = 15) -> Pos:
    def try_viable_direction() -> Pos | None:
        direction = get_rng().choice(tuple(Directions - parent.connected_directions()))
        match direction:
            case DirectionsEnum.NORTH:
                x = parent.pos.x + get_rng().randint(-size.width, parent.size.width + size.width)
                y = parent.pos.y - size.height - pad
            case DirectionsEnum.EAST:
                x = parent.pos.x + parent.size.width + pad
                y = parent.pos.y + get_rng().randint(-size.height, parent.size.height + size.height)
            case DirectionsEnum.SOUTH:
                x = parent.pos.x + get_rng().randint(-size.width, parent.size.width + size.width)
                y = parent.pos.y + parent.size.height + pad
            case DirectionsEnum.WEST:
                x = parent.pos.x - size.width - pad
                y = parent.pos.y + get_rng().randint(-size.height, parent.size.height + size.height)
            case _:
                raise AssertionError('Unhandled case')

        position = Pos(x, y)
        if not any([r.overlaps(Room(-1, position, size), pad) for r in rooms]):
            return position

        return None
    def search_nearby(padding_check: int) -> Pos | None:
        parent_center = parent.get_center()
        for dx in range(-search_radius, search_radius + 1):
            for dy in range(-search_radius, search_radius + 1):
                position = Pos(parent_center.x + dx, parent_center.y + dy)
                if not any([r.overlaps(Room(-1, position, size), padding_check) for r in rooms]):
                    return position
        return None

    pad = get_rng().choice(padding)
    if parent is None:
        return Pos(0, 0)

    for _ in range(max_attempts):
        if (pos := try_viable_direction()) is not None:
            return pos

    if (pos := search_nearby(pad)) is not None:
        return pos

    if (pos := search_nearby(padding[0])) is not None:
        return pos

    raise AssertionError('Could not place a room')

def create_rooms_from_graph(start: RoomNode, min_max_size: range = range(6,13), main_diff: int = 2, padding: range = range(2, 5)) -> dict[int, Room]:
    rooms = {}

    def place_room(node: RoomNode, parent: Room = None, depth=0):
        size = generate_room_size(node, min_max_size, main_diff)
        pos = find_room_pos(size, parent, padding, list(rooms.values()))

        room = Room(
            id=node.id,
            tag=node.tag,
            pos=pos,
            size=size
        )
        rooms[node.id] = room

        if parent:
            # TODO: Implement a real corridor connection
            door, parent_door = room.nearest_doors_indexes(parent)
            parent.add_connection(room, parent_door)
            room.add_connection(parent, door)

        for child in node.children:
            place_room(child, room, depth + 1)

    place_room(start)
    return rooms