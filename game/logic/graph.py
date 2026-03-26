from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Self
from ..utils import get_rng


class RoomTags(Enum):
    NORMAL = 0
    SPAWN = 1
    MAIN = 2
    BOSS = 3
    CHEST = 4
    # TRAP
    # SHOP

@dataclass()
class RoomNode:
    id: int
    depth: int
    connections: list[Self] = field(default_factory=list, init=False)
    parent: Self = field(init=False)
    tag: RoomTags = RoomTags.NORMAL

    def append(self, child: Self):
        self.connections.append(child)
        child.parent = self

def generate_graph(max_rooms = 20, bias_weight: dict[int, float] = None) -> RoomNode:
    rooms = [RoomNode(0, 0, RoomTags.SPAWN)]
    if bias_weight is None:
        bias_weight = {0: 1.25, 1: 1, 2: .75}

    for i in range (1, max_rooms):
        candidates = [r for r in rooms if len(r.connections) < 3]
        if not candidates:
            break

        weights = []
        for r in candidates:
            conn = len(r.connections)
            weights.append(bias_weight.get(conn, 0.1))

        parent = get_rng().choices(candidates, weights=weights, k=1)[0]
        new_room = RoomNode(i, parent.depth+1)
        parent.append(new_room)
        rooms.append(new_room)

    return rooms[0]

def find_longest_path(spawn: RoomNode) -> list[RoomNode]:
    visited = {spawn.id}
    queue = deque([spawn])
    last = spawn

    while queue:
        node = queue.popleft()
        visited.add(node.id)
        last = node

        for child in node.connections:
            queue.append(child)

    path = []
    while last.tag != RoomTags.SPAWN:
        path.append(last)
        last = last.parent

    path.reverse()

    for room in path:
        room.tag = RoomTags.MAIN
    path[-1].tag = RoomTags.BOSS

    return path

def print_nodes(node: RoomNode, visited=None, prefix="", is_last=True):
    if visited is None:
        visited = set()
    if node.id in visited:
        return
    visited.add(node.id)

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
        case RoomTags.CHEST:
            icon = 'C'
        case _:
            raise AssertionError(f"Unhandled case: {node.tag}")

    print(prefix + connector + f"{icon}{node.id}")

    new_prefix = prefix + ("   " if is_last else "│  ")

    children = [n for n in node.connections if n.id not in visited]

    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        print_nodes(child, visited, new_prefix, is_last_child)