from collections import deque
from dataclasses import dataclass, field
from typing import Callable

from game.domain.actions import Action
from game.ecs.components.shape import SetShape, Shape


@dataclass(slots=True)
class ActionQueue:
    actions: deque[Action] = field(default_factory=deque)


class FieldOfView(SetShape):
    pass


@dataclass(slots=True)
class InRoom:
    room: int | None


@dataclass(frozen=True, slots=True)
class Display:
    char: str
    priority: int = 0


@dataclass(slots=True)
class Trigger:
    shape: Shape
    on_enter: list[Callable] = field(default_factory=list)
    on_stay: list[Callable] = field(default_factory=list)
    on_exit: list[Callable] = field(default_factory=list)
    occupants: set[int] = field(default_factory=set)
