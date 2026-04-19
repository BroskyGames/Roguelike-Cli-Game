from collections import deque
from dataclasses import dataclass, field

from game.domain.actions import Action


@dataclass(slots=True)
class ActionQueue:
    actions: deque[Action] = field(default_factory=deque)


# @dataclass
# class AllowedActions:
#     actions: set[Action] = field(default_factory=set)


@dataclass(slots=True)
class ActionPoints:
    current: int
    max: int


@dataclass(frozen=True, slots=True)
class Speed:
    speed: int


@dataclass(slots=True)
class Health:
    health: int
    max_health: int


@dataclass(frozen=True, slots=True)
class Visible:
    pass


@dataclass(frozen=True, slots=True)
class Player:
    pass


@dataclass(slots=True)
class InRoom:
    room: int | None


@dataclass(frozen=True, slots=True)
class Display:
    char: str
