from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .core_types import Pos
    from ..map.tile_map import Tile


@dataclass(slots=True)
class GameState:
    seed: int = None
    rng_state: Any = None
    map: dict["Pos", "Tile"] = field(default_factory=dict)

    debug: bool = False
