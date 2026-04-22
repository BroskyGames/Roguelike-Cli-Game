from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any, TYPE_CHECKING

from game.core.geometry import Pos
from game.core.map_types import Tile

if TYPE_CHECKING:
    from game.map.layout import Room


class Phase(StrEnum):
    PLANNING = auto()
    RESOLUTION = auto()


@dataclass(slots=True)
class State:
    seed: int
    map: defaultdict[Pos, Tile]
    rooms: tuple[Room, ...]
    player: int
    last_room: int = 0

    rng_state: Any = None
    debug: bool = False

    phase: Phase = field(init=False, default=Phase.PLANNING)
