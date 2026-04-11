from abc import ABC
from dataclasses import dataclass
from enum import IntFlag, auto
from typing import Iterator, NamedTuple, Protocol, Self, runtime_checkable


@runtime_checkable
class IsPosition(Protocol):
    @property
    def x(self) -> int: ...

    @property
    def y(self) -> int: ...


class PositionOps(ABC):
    def __add__(self: Self, other: "Vector2") -> Self:
        if isinstance(other, Vector2):
            return self.__class__(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self: Self, other: IsPosition) -> "Vector2":
        if isinstance(other, IsPosition):
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


@dataclass(slots=True, frozen=True)
class Pos(PositionOps):
    x: int
    y: int


@dataclass(slots=True)
class MutablePos(PositionOps):
    x: int
    y: int

    def __iadd__(self: "MutablePos", other: IsPosition) -> "MutablePos":
        self.x += other.x
        self.y += other.y
        return self


@dataclass(slots=True, frozen=True)
class Vector2:
    x: int
    y: int

    def __iter__(self: Self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __getitem__(self: Self, index: int) -> int:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError

    def __neg__(self) -> "Vector2":
        return Vector2(-self.x, -self.y)


class Size(NamedTuple):
    width: int
    height: int


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


BaseDirections: set[Directions] = set(Directions)
DirectionsDiagonals: set[Directions] = set(Directions) | {Directions.NORTH | Directions.EAST,
                                                          Directions.EAST | Directions.SOUTH,
                                                          Directions.SOUTH | Directions.WEST,
                                                          Directions.WEST | Directions.NORTH}

if __name__ == "__main__":
    # print(Pos(3, 2) - Pos(3, 2))
    print((Directions.NORTH | Directions.EAST).vector())
