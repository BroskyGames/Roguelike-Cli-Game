from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from game.core.geometry import Pos
from game.core.map_types import Tile


@dataclass(slots=True)
class State:
    seed: int = None
    rng_state: Any = None
    map: dict[Pos, Tile] = field(default_factory=dict)
    curr_room: int = None
    camera_center: Pos = Pos(0, 0)

    debug: bool = False
