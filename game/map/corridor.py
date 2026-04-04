from dataclasses import dataclass
from functools import lru_cache
from heapq import heappush, heappop
from itertools import count
from typing import Callable

from .layout import Door, Room
from ..core.core_types import DirectionVectors, Pos, Vector2


@dataclass(slots=True)
class Corridor:
    path: list[Pos]
    connects: tuple[Door, Door]

MAX_SEARCH_DIST = 100

def door_exit(door: Door) -> Pos:
    return door.pos + DirectionVectors[door.direction]

def get_connection_doors(room: Room, target: Room) -> tuple[Door, Door]:
    door = room.doors[room.connections.index(target.id)]
    target_door = target.doors[target.connections.index(room.id)]
    return door, target_door

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

def astar(start: Pos, goal: Pos, is_blocked_fn: Callable[[Pos], bool], start_dir: Vector2, end_dir: Vector2) -> list[Pos]:
    heap = []
    counter = count()
    heappush(heap, (0, next(counter), start, None))

    came_from: dict[Pos, Pos] = {}
    g_score: dict[Pos, float] = {start: 0}

    while heap:
        _,  _, current, prev_dir = heappop(heap)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for move_dir in DirectionVectors.values():
            neighbor = current + move_dir

            if is_blocked_fn(neighbor):
                continue

            if manhattan(neighbor, start) > 100:
                continue

            start_penalty = 0 if (prev_dir is not None) or (move_dir == start_dir) else .1
            end_penalty = 0 if (neighbor != goal) or (move_dir == -end_dir) else .1

            tentative_g = g_score[current] + 1 + start_penalty + end_penalty

            if tentative_g < g_score.get(neighbor, 1_000_000):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan(neighbor, goal)

                heappush(heap, (
                    f,
                    next(counter),
                    neighbor,
                    move_dir
                ))
    print(start, goal)
    raise RuntimeError("No path found between doors")

def make_is_blocked_fn(rooms: list["Room"], corridors: list[Corridor], padding: int = 1) -> Callable[[Pos], bool]:
    @lru_cache(maxsize=1000)
    def is_blocked(pos: "Pos") -> bool:
        return any(
            room.x - padding <= pos.x <= room.x + room.width - 1 + padding and
            room.y - padding <= pos.y <= room.y + room.height - 1 + padding
            for room in rooms
        ) or any (
            abs(tile.x - pos.x) <= padding and
            abs(tile.y - pos.y) <= padding
            for corridor in corridors
            for tile in corridor.path
        )

    return is_blocked

def build_corridors(rooms: list[Room]) -> list[Corridor]:
    corridors = []

    for room in rooms:
        for target_id in room.connections:
            if room.id > target_id:
                continue

            target = rooms[target_id]
            door, target_door = get_connection_doors(room, target)

            start = door_exit(door)
            end = door_exit(target_door)

            path = astar(start, end, make_is_blocked_fn(rooms, corridors), DirectionVectors[door.direction], DirectionVectors[target_door.direction])

            corridors.append(Corridor(path, (door, target_door)))

    return corridors