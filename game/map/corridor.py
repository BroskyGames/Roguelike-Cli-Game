from __future__ import annotations

from dataclasses import dataclass
# from functools import lru_cache
from heapq import heappop, heappush
from itertools import count
from typing import Callable

from .layout import Door, Room
from ..core.geometry import BaseDirections, Directions, Pos


@dataclass(slots=True, frozen=True)
class Corridor:
    path: tuple[Pos, ...]
    connects: tuple[Door, Door]


MAX_SEARCH_DIST = 100


def door_exit(door: Door) -> Pos:
    return door.pos + door.direction.vector()


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def astar(start: Pos, goal: Pos, is_blocked_fn: Callable[[Pos], bool], start_dir: Directions, end_dir: Directions) -> \
        list[Pos]:
    heap = []
    counter = count()
    heappush(heap, (0, next(counter), start, None))

    came_from: dict[Pos, Pos] = {}
    g_score: dict[Pos, float] = {start: 0}

    while heap:
        _, _, current, prev_dir = heappop(heap)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for move_dir in BaseDirections:
            neighbor = current + move_dir.vector()

            if is_blocked_fn(neighbor):
                continue

            if manhattan(neighbor, start) > MAX_SEARCH_DIST:
                continue

            start_penalty = 0 if (prev_dir is not None) or (move_dir == start_dir) else .45
            end_penalty = 0 if (neighbor != goal) or (move_dir.vector() == -end_dir.vector()) else .45
            change_dir_penalty = 0 if prev_dir == move_dir else .1

            tentative_g = g_score[current] + 1 + start_penalty + end_penalty + change_dir_penalty

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
    raise RuntimeError("No path found between doors")


def make_is_blocked_fn(rooms: tuple[Room, ...], corridors: list[Corridor], allowed: set[Corridor], padding: int = 1) -> \
        Callable[[Pos], bool]:
    # @lru_cache(maxsize=500)
    def is_blocked(pos: Pos) -> bool:
        return any(
            room.x - padding <= pos.x <= room.x + room.width - 1 + padding and
            room.y - padding <= pos.y <= room.y + room.height - 1 + padding
            for room in rooms
        ) or any(
            abs(tile.x - pos.x) <= padding and
            abs(tile.y - pos.y) <= padding
            for corridor in corridors
            if corridor not in allowed
            for tile in corridor.path
        )

    return is_blocked


def build_corridors(rooms: tuple[Room, ...]) -> list[Corridor]:
    corridors: list[Corridor] = []

    for room in rooms:
        for door in room.doors:
            for target_door in door.connections:
                if room.id > target_door.belongs_to:
                    continue

                allowed: set[Corridor] = {c for c in corridors if door in c.connects or target_door in c.connects}

                start = door_exit(door)
                end = door_exit(target_door)

                path = astar(start, end, make_is_blocked_fn(rooms, corridors, allowed), door.direction,
                             target_door.direction)

                corridors.append(Corridor(tuple(path), (door, target_door)))

    return corridors
