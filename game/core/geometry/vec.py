from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Iterator


@dataclass(slots=True, frozen=True)
class Vector2:
    """x, y must be in [-511, 511]"""

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

    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y)
