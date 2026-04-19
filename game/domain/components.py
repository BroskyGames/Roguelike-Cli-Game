from collections import deque
from dataclasses import dataclass, field

from game.domain.actions import Action


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
class Speed:
    speed: int


@dataclass
class Health:
    health: int


class Visible:
    pass


class Player:
    pass
