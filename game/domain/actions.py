from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, fields
from typing import ClassVar

from game.core.geometry import Directions


@dataclass(frozen=True, slots=True)
class Action(ABC):
    ent: int
    base_cost: ClassVar[float]

    def str(self, only_player: bool = False):
        values = ", ".join(
            f"{f.name}={getattr(self, f.name)}"
            for f in fields(self)
            if not (only_player and f.name == "ent")
        )
        return f"{self.__class__.__name__}({values})"


@dataclass(frozen=True, slots=True)
class MoveAction(Action):
    dir: Directions
    base_cost: ClassVar[float] = 1


@dataclass(frozen=True, slots=True)
class AttackAction(Action):
    base_cost: ClassVar[float] = 1.5


@dataclass(frozen=True, slots=True)
class DashAction(Action):
    dir: Directions
    base_cost: ClassVar[float] = 2


@dataclass(frozen=True, slots=True)
class WaitAction(Action):
    base_cost: ClassVar[float] = 0.5


@dataclass(frozen=True, slots=True)
class EndTurnAction(Action):
    base_cost: ClassVar[float] = 0


@dataclass(frozen=True, slots=True)
class RemoveLastAction(Action):
    base_cost: ClassVar[float] = 0


@dataclass(frozen=True, slots=True)
class ClearQueueAction(Action):
    base_cost: ClassVar[float] = 0
