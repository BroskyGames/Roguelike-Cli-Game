from __future__ import annotations

import curses
from typing import Callable

from game.ui.layout import LayoutBuilder
from game.ui.rect import WindowRect
from .basic import Window

WindowFactory = dict[str, Callable[[WindowRect], Window]]


class WindowManager:
    def __init__(self, stdscr: curses.window, layout_builder: LayoutBuilder, windows_factory: WindowFactory):
        self.stdscr = stdscr
        self.layout_builder = layout_builder
        layout = self.layout_builder.build(*self.stdscr.getmaxyx())
        self.windows = {
            name: windows_factory[name](rect)
            for name, rect in layout.items()
            if name in windows_factory.keys()
        }
        print(layout)

    def handle_resize(self):
        curses.update_lines_cols()
        # self.stdscr.refresh()
        self.stdscr.clearok(True)
        layout = self.layout_builder.build(*self.stdscr.getmaxyx())
        for name, rect in layout.items():
            if name not in self.windows.keys():
                continue
            self.windows[name].resize(rect)
        self.draw()

    # def _draw_background(self):
    #     rows, cols = self.stdscr.getmaxyx()
    #     if rows > MAX_ROWS or cols > MAX_COLS:
    #         self.stdscr.bkgd(" ", curses.A_DIM)
    #         self.stdscr.erase()
    #         self.stdscr.noutrefresh()

    def draw(self):
        # self._draw_background()
        for window in self.windows.values():
            window.draw()
        curses.doupdate()
