from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from game.core.geometry import Directions


@dataclass(frozen=True, slots=True)
class Action(ABC):
    entity: int

    @property
    @abstractmethod
    def base_cost(self) -> float: ...


@dataclass(frozen=True, slots=True)
class MoveAction(Action):
    direction: Directions
    base_cost: ClassVar[float] = 1


@dataclass(frozen=True, slots=True)
class AttackAction(Action):
    direction: Directions
    weapon: Weapon | None = None
    base_cost: ClassVar[float] = 1.5


@dataclass(frozen=True, slots=True)
class DashAction(Action):
    direction: Directions
    base_cost: ClassVar[float] = 2


@dataclass(frozen=True, slots=True)
class WaitAction(Action):
    base_cost: ClassVar[float] = .5
