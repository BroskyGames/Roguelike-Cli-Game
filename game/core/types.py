from dataclasses import dataclass
from enum import IntEnum, auto
from typing import NamedTuple


class Pos(NamedTuple):
    x: int
    y: int

class Vector2(NamedTuple):
    x: int
    y: int

class Size(NamedTuple):
    width: int
    height: int

@dataclass(slots=True)
class MutablePos:
    x: int
    y: int

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