from collections import defaultdict
from dataclasses import dataclass, field

from game.domain.map_types import Tile
from game.map import Room

from .geometry import Pos


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
