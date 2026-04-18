from collections import deque
from dataclasses import dataclass, field
from typing import Final

from game.core.actions import Action


@dataclass
class ActionQueue:
    actions: deque[Action] = field(default_factory=deque)


@dataclass
class AllowedActions:
    actions: set[Action] = field(default_factory=set)


@dataclass
class ActionPoints:
    current: int
    max: int


@dataclass
class Health:
    health: int


@dataclass
class DashSpeed:
    speed: int


IsPlayer = Final[bool]
