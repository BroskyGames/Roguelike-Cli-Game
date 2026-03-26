from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Self
from ..utils import bfs, get_rng


class RoomTags(Enum):
    NORMAL = auto()
    SPAWN = auto()
    MAIN = auto()
    BOSS = auto()
    TREASURE = auto()
    TRAP = auto()
    # SHOP

@dataclass()
class RoomNode:
    id: int
    depth: int
    children: list[Self] = field(default_factory=list, init=False)
    parent: Self = field(init=False)
    tag: RoomTags = RoomTags.NORMAL

    def append(self, child: Self):
        self.children.append(child)
        child.parent = self

def generate_graph(max_rooms = 20, bias_weight: dict[int, float] = None) -> RoomNode:
    rooms = [RoomNode(0, 0, RoomTags.SPAWN)]
    if bias_weight is None:
        bias_weight = {0: 1.25, 1: 1, 2: .75, 3: .4}

    for i in range (1, max_rooms):
        candidates = [r for r in rooms if len(r.children) < 3 or
                      (r.tag == RoomTags.SPAWN and len(r.children) > 4)]
        if not candidates:
            break

        weights = []
        for r in candidates:
            conn = len(r.children)
            weights.append(bias_weight.get(conn, 0.1))

        parent = get_rng().choices(candidates, weights=weights, k=1)[0]
        new_room = RoomNode(i, parent.depth+1)
        parent.append(new_room)
        rooms.append(new_room)

    return rooms[0]

def distribute_tags(spawn: RoomNode, treasure_chance: float, trap_chances: float) -> None:
    rng = get_rng()
    # Main path, Boss room
    def return_room(r: RoomNode, _: RoomNode) -> RoomNode:
        return r
    last = bfs(spawn, return_room)
    last.tag = RoomTags.BOSS
    last = last.parent
    while last.tag != RoomTags.SPAWN:
        last.tag = RoomTags.MAIN
        last = last.parent

    # Treasure rooms
    def detect_treasure_rooms(r: RoomNode, arr: list[RoomNode]) -> list[RoomNode]:
        if arr is None:
            arr = []
        return arr + [r] if len(r.children) == 0 and r.tag != RoomTags.BOSS and rng.random() < treasure_chance else arr
    for room in bfs(spawn, detect_treasure_rooms):
        room.tag = RoomTags.TREASURE

    # Traps
    def detect_trap_rooms(r: RoomNode, arr: list[RoomNode]) -> list[RoomNode]:
        if arr is None:
            arr = []
        return arr + [r] if r.tag == RoomTags.NORMAL and rng.random() < trap_chances else arr

    for room in bfs(spawn, detect_trap_rooms):
        room.tag = RoomTags.TRAP

def find_longest_path(spawn: RoomNode) -> list[RoomNode]:
    last = bfs(spawn, lambda r, *_: r)

    path = []
    while last.tag != RoomTags.SPAWN:
        path.append(last)
        last = last.parent

    path.reverse()

    for room in path:
        room.tag = RoomTags.MAIN
    path[-1].tag = RoomTags.BOSS

    return path

def print_nodes(node: RoomNode,  prefix="", is_last=True):
    connector = "└─ " if is_last else "├─ "
    match node.tag:
        case RoomTags.NORMAL:
            icon = 'N'
        case RoomTags.SPAWN:
            icon = 'S'
        case RoomTags.MAIN:
            icon = 'M'
        case RoomTags.BOSS:
            icon = 'B'
        case RoomTags.TREASURE:
            icon = 'C'
        case RoomTags.TRAP:
            icon = 'T'
        case _:
            raise AssertionError(f"Unhandled case: {node.tag}")

    print(prefix + connector + f"{icon}{node.id}")

    new_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(node.children):
        is_last_child = i == len(node.children) - 1
        print_nodes(child, new_prefix, is_last_child)