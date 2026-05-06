from __future__ import annotations

from dataclasses import dataclass
from enum import IntFlag, auto
from typing import ClassVar, Iterator, NamedTuple, Self


@dataclass(slots=True, frozen=True)
class Pos:
    # x, y must be in [-511, 511]
    x: int
    y: int

    MASK: ClassVar[int] = (1 << 10) - 1

    def __add__(self: Pos, other: Vector2) -> Pos:
        if isinstance(other, Vector2):
            return Pos(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self: Self, other: Pos) -> Vector2:
        if isinstance(other, Pos):
            return Vector2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __iter__(self: Self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __getitem__(self: Self, index: int) -> int:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError

    def __hash__(self) -> int:
        return (self.x << 10) | (self.y & self.MASK)


@dataclass(slots=True, frozen=True)
class Vector2:
    # x, y must be in [-511, 511]
    x: int
    y: int
    MASK: ClassVar[int] = (1 << 10) - 1

    def __add__(self: Vector2, other: Vector2) -> Vector2:
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError

    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)

    def __hash__(self) -> int:
        return (self.x << 10) | (self.y & self.MASK)


class Size(NamedTuple):
    # w, h must be in [1, 32]
    width: int
    height: int
    MASK: ClassVar[int] = (1 << 5) - 1

    def __iter__(self) -> Iterator[int]:
        yield self.width
        yield self.height

    def __hash__(self) -> int:
        return (self.width << 5) | (self.height & self.MASK)


class Directions(IntFlag):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def vector(self):
        x = 0
        y = 0
        if self & Directions.NORTH:
            y -= 1
        if self & Directions.SOUTH:
            y += 1
        if self & Directions.EAST:
            x += 1
        if self & Directions.WEST:
            x -= 1
        return Vector2(x, y)

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name_}>"

    def __str__(self):
        return f"{self._name_}"


BaseDirections: set[Directions] = set(Directions)
DirectionsDiagonals: set[Directions] = set(Directions) | {Directions.NORTH | Directions.EAST,
                                                          Directions.EAST | Directions.SOUTH,
                                                          Directions.SOUTH | Directions.WEST,
                                                          Directions.WEST | Directions.NORTH}

DIRECTION_VECTORS: dict[Directions, Vector2] = {d: d.vector() for d in DirectionsDiagonals}

if __name__ == "__main__":
    # print(Pos(3, 2) - Pos(3, 2))
    print((Directions.NORTH | Directions.EAST).vector())
