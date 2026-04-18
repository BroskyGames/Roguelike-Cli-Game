from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from game.core.geometry import Pos
from game.core.map_types import Tile

if TYPE_CHECKING:
    from game.map.layout import Room


@dataclass(slots=True)
class State:
    seed: int
    map: dict[Pos, Tile]
    rooms: tuple[Room, ...]
    last_room: int = 0

    rng_state: Any = None
    debug: bool = False
