from collections import deque
from dataclasses import dataclass, field
from enum import StrEnum, auto
from ..utils import Reducer, combine_reducers, get_rng


class RoomTags(StrEnum):
    NORMAL = 'N'
    SPAWN = 'S'
    MAIN = 'M'
    BOSS = 'B'
    GENETIC = 'G'
    TRAP = 'T'
    # SHOP

@dataclass()
class RoomNode:
    """Node that represents abstract form of room to be used as a base for graph structure"""
    id: int
    depth: int
    children: list["RoomNode"] = field(default_factory=list, init=False)
    parent: "RoomNode" = field(init=False)
    tag: RoomTags = RoomTags.NORMAL

    def append(self, child: "RoomNode"):
        self.children.append(child)
        child.parent = self

def bfs[T](start: RoomNode, reducer: Reducer[T, RoomNode]) -> T:
    queue = deque([start])
    while queue:
        node = queue.popleft()
        reducer(node)
        for child in node.children:
            queue.append(child)
    return reducer.acc

def generate_graph(max_rooms = 20, bias_weight: dict[int, float] = None) -> RoomNode:
    rooms = [RoomNode(0, 0, RoomTags.SPAWN)]
    if bias_weight is None:
        bias_weight = {0: 1.25, 1: 1, 2: .75}

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

def assign_tags(spawn: RoomNode, genetic_chance: float, trap_chances: float) -> None:
    rng = get_rng()

    def return_room(r: RoomNode, _: None) -> RoomNode:
        return r

    def assign_genetic_labs(r: RoomNode, _: None) -> None:
        if len(r.children) == 0 and rng.random() < genetic_chance:
            r.tag = RoomTags.GENETIC

    def assign_trap_rooms(r: RoomNode, _: None) -> None:
        if r.tag == RoomTags.NORMAL and rng.random() < trap_chances:
            r.tag = RoomTags.TRAP

    last = bfs(spawn, combine_reducers(
        Reducer(return_room, None),
        Reducer(assign_genetic_labs, None),
        Reducer(assign_trap_rooms, None)))[0]

    last.tag = RoomTags.BOSS
    last = last.parent

    while last.tag != RoomTags.SPAWN:
        last.tag = RoomTags.MAIN
        last = last.parent

def print_nodes(node: RoomNode,  prefix="", is_last=True):
    connector = "└─ " if is_last else "├─ "

    print(prefix + connector + f"{node.tag.value}{node.id}")

    new_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(node.children):
        is_last_child = i == len(node.children) - 1
        print_nodes(child, new_prefix, is_last_child)