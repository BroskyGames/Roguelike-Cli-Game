from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Protocol, Self

from game.core.geometry import Pos, Size


class Shape(Protocol):
    def contains(self, pos: Pos) -> bool: ...
    def flatten(self) -> Iterator[Pos]: ...


@dataclass(slots=True, frozen=True)
class RectShape:
    x: int
    y: int
    w: int
    h: int

    @classmethod
    def from_pos_size(cls, pos: Pos, size: Size) -> Self:
        return cls(pos.x, pos.y, size.width, size.height)

    def contains(self, pos: Pos) -> bool:
        return self.x <= pos.x < self.x + self.w and self.y <= pos.y < self.y + self.h

    def flatten(self) -> Iterator[Pos]:
        for dx in range(self.w):
            for dy in range(self.h):
                yield Pos(self.x + dx, self.y + dy)


@dataclass(slots=True, frozen=True)
class CircleShape:
    x: int
    y: int
    r: int
    r2: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "r2", self.r * self.r)

    @classmethod
    def from_pos_radius(cls, pos: Pos, radius: int) -> Self:
        return cls(pos.x, pos.y, radius)

    def contains(self, pos: Pos) -> bool:
        dx = pos.x - self.x
        dy = pos.y - self.y
        return dx * dx + dy * dy <= self.r2

    def flatten(self) -> Iterator[Pos]:
        for dx in range(-self.r, self.r + 1):
            for dy in range(-self.r, self.r + 1):
                pos = Pos(self.x + dx, self.y + dy)
                if self.contains(pos):
                    yield pos


@dataclass(slots=True, frozen=True)
class SetShape:
    shape: frozenset[Pos] = field(default_factory=frozenset)

    def contains(self, pos: Pos) -> bool:
        return pos in self.shape

    def flatten(self) -> Iterator[Pos]:
        return iter(self.shape)


@dataclass(slots=True, frozen=True)
class PointShape:
    x: int
    y: int

    @classmethod
    def from_pos(cls, pos: Pos) -> Self:
        return cls(pos.x, pos.y)

    def contains(self, pos: Pos) -> bool:
        return self.x == pos.x and self.y == pos.y

    def flatten(self) -> Iterator[Pos]:
        yield Pos(self.x, self.y)
