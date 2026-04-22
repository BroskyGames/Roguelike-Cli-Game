from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from random import Random

from ..core.map_types import RoomTypes
from ..utils import Reducer, combine_reducers


@dataclass(slots=True)
class RoomNode:
    """Node that represents abstract form of room to be used as a base for graph structure"""
    id: int
    depth: int
    children: list[RoomNode] = field(default_factory=list, init=False)
    parent: RoomNode = field(init=False, default=None)
    type: RoomTypes = RoomTypes.NORMAL

    def append(self, child: RoomNode):
        self.children.append(child)
        child.parent = self


def generate_graph(rng: Random, rooms_amount=20, bias_weight=None) -> RoomNode:
    rooms = [RoomNode(0, 0, RoomTypes.SPAWN)]

    if bias_weight is None:
        bias_weight = {0: 1.25, 1: 1, 2: .75}

    for i in range(1, rooms_amount):
        candidates = [r for r in rooms if len(r.children) < 3 or
                      (r.type == RoomTypes.SPAWN and len(r.children) > 4)]
        if not candidates:
            break

        weights = []
        for r in candidates:
            conn = len(r.children)
            weights.append(bias_weight.get(conn, 0.1))

        parent = rng.choices(candidates, weights=weights, k=1)[0]
        new_room = RoomNode(i, parent.depth + 1)
        parent.append(new_room)
        rooms.append(new_room)

    return rooms[0]


def assign_tags(spawn: RoomNode, rng: Random, genetic_chance: float, trap_chances: float) -> None:
    def return_room(r: RoomNode, _: None) -> RoomNode:
        return r

    def assign_genetic_labs(r: RoomNode, _: None) -> None:
        if len(r.children) == 0 and rng.random() < genetic_chance:
            r.type = RoomTypes.GENETIC

    def assign_trap_rooms(r: RoomNode, _: None) -> None:
        if r.type == RoomTypes.NORMAL and rng.random() < trap_chances:
            r.type = RoomTypes.TRAP

    last = bfs(spawn, combine_reducers(
        Reducer(return_room, None),
        Reducer(assign_genetic_labs, None),
        Reducer(assign_trap_rooms, None)))[0]

    last.type = RoomTypes.BOSS
    last = last.parent

    while last.parent is not None:
        last.type = RoomTypes.MAIN
        last = last.parent


def bfs[T](start: RoomNode, reducer: Reducer[T, RoomNode]) -> T:
    queue = deque([start])
    while queue:
        node = queue.popleft()
        reducer(node)
        for child in node.children:
            queue.append(child)
    return reducer.acc
