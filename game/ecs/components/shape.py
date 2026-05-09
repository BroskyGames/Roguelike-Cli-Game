from dataclasses import InitVar, dataclass, field
from typing import Protocol, Self

from game.core.geometry import Pos, Size


class Shape(Protocol):
    def contains(self, pos: Pos) -> bool: ...


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


@dataclass(slots=True, frozen=True)
class CircleShape:
    x: int
    y: int
    r2: int = field(init=False)

    r: InitVar[int]

    def __post_init__(self, r: int):
        object.__setattr__(self, "r2", r * r)

    @classmethod
    def from_pos_radius(cls, pos: Pos, radius: int) -> Self:
        return cls(pos.x, pos.y, radius)

    def contains(self, pos: Pos) -> bool:
        dx = pos.x - self.x
        dy = pos.y - self.y
        return dx * dx + dy * dy <= self.r2


@dataclass(slots=True, frozen=True)
class SetShape:
    shape: frozenset[Pos] = field(default_factory=frozenset)

    def contains(self, pos: Pos) -> bool:
        return pos in self.shape


@dataclass(slots=True, frozen=True)
class PointShape:
    x: int
    y: int

    @classmethod
    def from_pos(cls, pos: Pos) -> Self:
        return cls(pos.x, pos.y)

    def contains(self, pos: Pos) -> bool:
        return self.x == pos.x and self.y == pos.y
