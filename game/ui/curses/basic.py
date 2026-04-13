from __future__ import annotations

import curses
from abc import ABC, abstractmethod

from .rect import WindowRect


class Window(ABC):

    def __init__(self, rect: WindowRect):
        self.win = curses.newwin(*rect)

    def resize(self, rect: WindowRect) -> None:
        try:
            self.win.resize(rect.lines, rect.cols)
            self.win.mvwin(rect.y, rect.x)
        except curses.error:
            self.win = curses.newwin(*rect)

    @abstractmethod
    def draw(self) -> None:
        """self.win.noutrefresh() call required"""
        ...
