from __future__ import annotations

import curses
from abc import ABC, abstractmethod

from game.ui.rect import Rect


class Window(ABC):

    def __init__(self, rect: Rect):
        self.win = curses.newwin(*rect)

    def resize(self, rect: Rect) -> None:
        try:
            self.win.resize(rect.h, rect.w)
            self.win.mvwin(rect.y, rect.x)
        except curses.error:
            self.win = curses.newwin(*rect)

    @abstractmethod
    def draw(self) -> None:
        """self.win.noutrefresh() call required"""
        ...
