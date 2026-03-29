from dataclasses import dataclass
from enum import IntEnum, auto
from typing import NamedTuple

class Pos(NamedTuple):
    x: int
    y: int

class Size(NamedTuple):
    width: int
    height: int

@dataclass
class MutablePos:
    x: int
    y: int

class DirectionsEnum(IntEnum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

Directions = {DirectionsEnum.NORTH, DirectionsEnum.EAST, DirectionsEnum.SOUTH, DirectionsEnum.WEST}
