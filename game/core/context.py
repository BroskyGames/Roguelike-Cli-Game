from collections import defaultdict
from dataclasses import dataclass, field

from game.core.geometry import Pos
from game.core.map_types import Tile
from game.map import Room


@dataclass
class Context:
    map: defaultdict[Pos, Tile]
    rooms: tuple[Room, ...]

    player: int
    last_room: int = 0

    explored: set[Pos] = field(init=False, default_factory=set)
