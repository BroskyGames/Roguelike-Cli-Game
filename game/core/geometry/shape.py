from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Iterator, Protocol, Self

from .pos import Pos
from .size import Size


class Shape(Protocol):
    def contains(self, pos: Pos) -> bool: ...
    def flatten(self) -> Iterator[Pos]: ...


@dataclass(slots=True, frozen=True)
class RectShape:
    """
    x, y in [-511, 511]
    w, h in [1, 32]
    """

    x: int
    y: int
    w: int
    h: int
    MASK_SIZE: ClassVar[int] = (1 << 5) - 1
    MASK_POS: ClassVar[int] = (1 << 10) - 1

    @classmethod
    def from_pos_size(cls, pos: Pos, size: Size) -> Self:
        return cls(pos.x, pos.y, size.w, size.h)

    def contains(self, pos: Pos) -> bool:
        return self.x <= pos.x < self.x + self.w and self.y <= pos.y < self.y + self.h

    def flatten(self) -> Iterator[Pos]:
        for dx in range(self.w):
            for dy in range(self.h):
                yield Pos(self.x + dx, self.y + dy)

    def __hash__(self) -> int:
        return (
            (self.x << 20)
            | ((self.y & self.MASK_POS) << 10)
            | ((self.w & self.MASK_SIZE) << 5)
            | (self.h & self.MASK_SIZE)
        )


@dataclass(slots=True, frozen=True)
class CircleShape:
    """
    x, y in [-511, 511]
    r in [1, 16]
    """

    x: int
    y: int
    r: int
    r2: int = field(init=False)
    MASK_POS: ClassVar[int] = (1 << 10) - 1
    MASK_RADIUS: ClassVar[int] = (1 << 4) - 1

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

    def __hash__(self) -> int:
        return (
            (self.x << 14)
            | ((self.y & self.MASK_POS) << 4)
            | (self.r & self.MASK_RADIUS)
        )


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
    MASK: ClassVar[int] = (1 << 10) - 1

    @classmethod
    def from_pos(cls, pos: Pos) -> Self:
        return cls(pos.x, pos.y)

    def contains(self, pos: Pos) -> bool:
        return self.x == pos.x and self.y == pos.y

    def flatten(self) -> Iterator[Pos]:
        yield Pos(self.x, self.y)

    def __hash__(self) -> int:
        return (self.x << 10) | (self.y & self.MASK)
