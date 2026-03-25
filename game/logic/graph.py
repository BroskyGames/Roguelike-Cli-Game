from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from pprint import pprint
from typing import Self, Optional
from ..utils import Pos, Size, get_rng, init_rng

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
    """
    [depth] is relative to spawn
    first element of [connections] is parent node
    """
    id: int
    depth: int
    connections: list[Self] = field(default_factory=list, init=False)
    tag: RoomTags = RoomTags.NORMAL

def generate_graph(max_rooms = 20, bias_weight: dict[int, float] = None) -> RoomNode:
    rooms = [RoomNode(0, 0, RoomTags.SPAWN)]
    if bias_weight is None:
        bias_weight = {0: .1, 1: 1.5, 2: 1, 3: .75,  4: .5}

    for i in range (1, max_rooms):
        candidates = [r for r in rooms if len(r.connections) < 4]
        if not candidates:
            break

        weights = []
        for r in candidates:
            conn = len(r.connections)
            weights.append(bias_weight.get(conn, 0.1))

        parent = get_rng().choices(candidates, weights=weights, k=1)[0]
        new_room = RoomNode(i, parent.depth+1)
        parent.connections.append(new_room)
        new_room.connections.append(parent)
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
            if child.id not in visited:
                queue.append(child)

    path = []
    while last.tag != RoomTags.SPAWN:
        path.append(last)
        last = last.connections[0]

    path.reverse()

    for room in path:
        room.tag = RoomTags.MAIN
    path[-1].tag = RoomTags.BOSS
    return path