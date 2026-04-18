from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from game.core.geometry import Directions


@dataclass(frozen=True, slots=True)
class Action(ABC):
    entity: int

    @property
    @abstractmethod
    def base_cost(self) -> float:
        ...


@dataclass(frozen=True, slots=True)
class MoveAction(Action):
    direction: Directions
    base_cost: float = 1


@dataclass(frozen=True, slots=True)
class AttackAction(Action):
    target: int
    base_cost: float = 1.5
