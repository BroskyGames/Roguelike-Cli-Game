from __future__ import annotations

from dataclasses import dataclass

# from functools import lru_cache
from heapq import heappop, heappush
from itertools import count
from typing import Callable

from game.core.geometry import BaseDirections, DIRECTION_VECTORS, Directions, Pos
from .room import Door, Room


@dataclass(slots=True, frozen=True)
class Corridor:
    path: tuple[Pos, ...]
    connects: tuple[Door, Door]


MAX_SEARCH_DIST = 100


def build_corridors(rooms: tuple[Room, ...]) -> list[Corridor]:
    corridors: list[Corridor] = []
    blocked = _make_blocked_set(rooms)

    for room in rooms:
        for door in room.doors:
            for target_door in door.connections:
                if room.id > target_door.belongs_to:
                    continue

                allowed: set[Pos] = {
                    Pos(tile_x + dx, tile_y + dy)
                    for c in corridors
                    if door in c.connects or target_door in c.connects
                    for tile_x, tile_y in c.path
                    for dx in range(-1, 2)
                    for dy in range(-1, 2)
                }

                is_blocked = _make_is_blocked_fn(blocked, allowed)

                start = _get_door_exit(door)
                end = _get_door_exit(target_door)

                path = _astar(
                    start, end, is_blocked, door.direction, target_door.direction
                )

                corridor = Corridor(tuple(path), (door, target_door))
                corridors.append(corridor)
                _add_corridor_to_blocked(blocked, corridor)

    return corridors


def _astar(
    start: Pos,
    goal: Pos,
    is_blocked_fn: Callable[[Pos], bool],
    start_dir: Directions,
    end_dir: Directions,
) -> list[Pos]:
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
            neighbor = current + DIRECTION_VECTORS[move_dir]

            if is_blocked_fn(neighbor):
                continue

            if _manhattan(neighbor, start) > MAX_SEARCH_DIST:
                continue

            start_penalty = (
                0 if (prev_dir is not None) or (move_dir == start_dir) else 0.45
            )
            end_penalty = (
                0
                if (neighbor != goal)
                or (DIRECTION_VECTORS[move_dir] == -DIRECTION_VECTORS[end_dir])
                else 0.45
            )
            change_dir_penalty = 0 if prev_dir == move_dir else 0.1

            tentative_g = (
                g_score[current] + 1 + start_penalty + end_penalty + change_dir_penalty
            )

            if tentative_g < g_score.get(neighbor, 1_000_000):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + _manhattan(neighbor, goal)

                heappush(heap, (f, next(counter), neighbor, move_dir))
    raise RuntimeError("No path found between doors")


def _make_is_blocked_fn(blocked: set[Pos], allowed: set[Pos]) -> Callable[[Pos], bool]:
    def is_blocked(pos: Pos) -> bool:
        return pos not in allowed and pos in blocked

    return is_blocked


def _make_blocked_set(rooms: tuple[Room, ...], padding: int = 1) -> set[Pos]:
    blocked: set[Pos] = set()

    for room in rooms:
        room_x, room_y = room.pos
        room_w, room_h = room.size
        for x in range(room_x - padding, room_x + room_w + padding):
            blocked.add(Pos(x, room_y - padding))
            blocked.add(Pos(x, room_y + room_h - 1 + padding))
        for y in range(room_y - padding, room_y + room_h + padding):
            blocked.add(Pos(room_x - padding, y))
            blocked.add(Pos(room_x + room_w - 1 + padding, y))

    return blocked


def _add_corridor_to_blocked(blocked: set[Pos], corridor: Corridor, padding: int = 1):
    for tile in corridor.path:
        x = tile.x
        y = tile.y
        for dx in range(-padding, padding + 1):
            for dy in range(-padding, padding + 1):
                blocked.add(Pos(x + dx, y + dy))


def _get_door_exit(door: Door) -> Pos:
    return door.pos + DIRECTION_VECTORS[door.direction]


def _manhattan(a: Pos, b: Pos) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)
