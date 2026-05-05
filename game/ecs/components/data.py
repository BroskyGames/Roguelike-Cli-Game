from collections import deque
from dataclasses import dataclass, field

from game.core.geometry import Pos
from game.domain.actions import Action


@dataclass(slots=True)
class ActionQueue:
    actions: deque[Action] = field(default_factory=deque)


@dataclass(slots=True)
class FieldOfView:
    visible: set[Pos] = field(default_factory=set)


@dataclass(slots=True)
class InRoom:
    room: int | None


@dataclass(frozen=True, slots=True)
class Display:
    char: str
    priority: int = 0
