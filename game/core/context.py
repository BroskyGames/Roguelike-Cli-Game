from collections import defaultdict
from dataclasses import dataclass, field

from game.core.geometry.pos import Pos
from game.core.map_types import Tile
from game.map import Room


@dataclass
class Context:
    map: dict[Pos, Tile]
    rooms: tuple[Room, ...]

    player: int = field(init=False)
    last_room: int = field(init=False, default=0)
    entities_index: defaultdict[Pos, set[int]] = field(
        init=False, default_factory=lambda: defaultdict(set)
    )

    explored: set[Pos] = field(init=False, default_factory=set)
