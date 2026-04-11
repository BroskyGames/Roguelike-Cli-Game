from __future__ import annotations

import curses
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.core.state import GameState
    from .rect import WindowRect


class GameWindow(ABC):
    def __init__(self, rect: WindowRect):
        self.win = curses.newwin(*rect)

    def resize(self, rect) -> None:
        self.win = curses.newwin(*rect)

    @abstractmethod
    def draw(self, state: GameState) -> None: ...
