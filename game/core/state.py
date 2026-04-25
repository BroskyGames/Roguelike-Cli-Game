from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Any, TYPE_CHECKING

from game.core.context import Context

if TYPE_CHECKING:
    pass


class Phase(StrEnum):
    PLANNING = auto()
    RESOLUTION = auto()


@dataclass(slots=True)
class State:
    context: Context

    seed: int
    rng_state: Any = None
    debug: bool = False

    phase: Phase = field(init=False, default=Phase.PLANNING)
