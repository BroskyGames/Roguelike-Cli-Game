from dataclasses import dataclass, field
from typing import Self

from .graph import RoomTags
from ..utils import Pos


@dataclass
class Room:
    x: int
    y: int
    width: int
    height: int
    tag: RoomTags = RoomTags.NORMAL
    doors: list[Pos] = field(default_factory=list)
    connections: list[Self] = field(default_factory=list)