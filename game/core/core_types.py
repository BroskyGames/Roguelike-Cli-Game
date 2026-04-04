from abc import ABC
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Iterator, Literal, NamedTuple, Protocol, Self, runtime_checkable


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

class DirectionsEnum(IntEnum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

Directions = {DirectionsEnum.NORTH, DirectionsEnum.EAST, DirectionsEnum.SOUTH, DirectionsEnum.WEST}

DirectionVectors = {
    DirectionsEnum.NORTH: Vector2(0, -1),
    DirectionsEnum.EAST:  Vector2(1, 0),
    DirectionsEnum.SOUTH: Vector2(0, 1),
    DirectionsEnum.WEST:  Vector2(-1, 0),
}

if __name__ == "__main__":
    print(Pos(3, 2) - Pos(3, 2))