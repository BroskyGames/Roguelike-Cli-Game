from dataclasses import dataclass
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

