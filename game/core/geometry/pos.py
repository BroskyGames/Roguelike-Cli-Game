from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Iterator

from .vec import Vector2


@dataclass(slots=True, frozen=True)
class Pos:
    """x, y must be in [-511, 511]"""

    x: int
    y: int

    MASK: ClassVar[int] = (1 << 10) - 1

    def __add__(self: Pos, other: Vector2) -> Pos:
        if isinstance(other, Vector2):
            return Pos(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other: Pos) -> Vector2:
        if isinstance(other, Pos):
            return Vector2(self.x - other.x, self.y - other.y)
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

    def __hash__(self) -> int:
        return (self.x << 10) | (self.y & self.MASK)


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)
