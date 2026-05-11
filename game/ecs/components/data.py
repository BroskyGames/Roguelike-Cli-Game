from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable

from game.core.geometry import Pos
from game.core.geometry.shape import SetShape, Shape
from game.domain.actions import Action

# --- Entities ---


@dataclass(slots=True)
class ActionQueue:
    actions: deque[Action] = field(default_factory=deque)


class FieldOfView(SetShape):
    pass


class AIType(Enum):
    BASIC = auto()


@dataclass(frozen=True, slots=True)
class AI:
    type: AIType = AIType.BASIC


@dataclass(slots=True)
class InRoom:
    room: int | None


@dataclass(frozen=True, slots=True)
class Display:
    char: str
    priority: int = 0


@dataclass(slots=True)
class Memory:
    pos: Pos
    display: Display


class DoorState(Enum):
    OPEN = auto()
    LOCKED = auto()


# --- Places ---

type TriggerCallback = Callable[[int, int], None]


@dataclass(slots=True)
class Trigger:
    shape: Shape
    on_enter: list[TriggerCallback] = field(init=False, default_factory=list)
    inside: list[TriggerCallback] = field(init=False, default_factory=list)
    on_exit: list[TriggerCallback] = field(init=False, default_factory=list)
    occupants: set[int] = field(init=False, default_factory=set)


@dataclass(slots=True, frozen=True)
class Doors:
    doors: frozenset[int]
