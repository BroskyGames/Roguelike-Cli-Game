from __future__ import annotations

import curses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .layout import MAX_COLS, MAX_ROWS, UILayout
    from .basic import GameWindow
    from game.core.state import GameState


class WindowManager:
    __slots__ = ('stdscr', 'windows', "_layout")

    def __init__(self, stdscr: curses.window, layout: UILayout):
        self.stdscr = stdscr
        self.windows: list[GameWindow] = []
        self._layout = layout
        self._build()

    def _build(self):
        rects = self._layout.layout_fn(*self.stdscr.getmaxyx())
        self.windows = [cls(*rect) for cls, rect in zip(self._layout.window_types, rects)]

    def handle_resize(self):
        curses.endwin()
        self.stdscr.refresh()
        rows, cols = self.stdscr.getmaxyx()
        dims = self._layout.layout_fn(rows, cols)
        for window, dim in zip(self.windows, dims):
            window.resize(*dim)

    def _draw_background(self):
        rows, cols = self.stdscr.getmaxyx()
        if rows > MAX_ROWS or cols > MAX_COLS:
            self.stdscr.bkgd(" ", curses.A_DIM)
            self.stdscr.erase()
            self.stdscr.noutrefresh()

    def draw(self, state: GameState):
        self._draw_background()
        
        for window in self.windows:
            window.draw(state)
            window.win.noutrefresh()
        curses.doupdate()
