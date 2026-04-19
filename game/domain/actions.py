from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from game.core.geometry import Directions


@dataclass(frozen=True, slots=True)
class Action(ABC):
    entity: int
    base_cost: ClassVar[float]


@dataclass(frozen=True, slots=True)
class MoveAction(Action):
    direction: Directions
    base_cost: ClassVar[float] = 1


@dataclass(frozen=True, slots=True)
class AttackAction(Action):
    base_cost: ClassVar[float] = 1.5


@dataclass(frozen=True, slots=True)
class DashAction(Action):
    direction: Directions
    base_cost: ClassVar[float] = 2


@dataclass(frozen=True, slots=True)
class WaitAction(Action):
    base_cost: ClassVar[float] = .5


@dataclass(frozen=True, slots=True)
class EndTurnAction(Action):
    base_cost: ClassVar[float] = 0


@dataclass(frozen=True, slots=True)
class RemoveLastAction(Action):
    base_cost: ClassVar[float] = 0


@dataclass(frozen=True, slots=True)
class ClearQueueAction(Action):
    base_cost: ClassVar[float] = 0
