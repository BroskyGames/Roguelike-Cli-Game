from typing import Callable

from game.ui.curses.basic import Window
from game.ui.curses.rect import WindowRect


class BorderedWindow(Window):
    def __init__(self, rect: WindowRect, inner_factory: Callable[[WindowRect], Window]):
        super().__init__(rect)
        inner_rect = self._inner_rect(rect)
        self._inner = inner_factory(inner_rect)

    @staticmethod
    def _inner_rect(rect: WindowRect) -> WindowRect:
        return WindowRect(rect.lines - 2, rect.cols - 2, rect.y + 1, rect.x + 1)

    def resize(self, rect: WindowRect) -> None:
        super().resize(rect)
        self._inner.resize(self._inner_rect(rect))

    def draw(self) -> None:
        self.win.erase()
        self.win.border()
        self.win.noutrefresh()
        self._inner.draw()


def bordered(inner_factory: Callable[[WindowRect], Window]) -> Callable[[WindowRect], Window]:
    def factory(rect: WindowRect) -> BorderedWindow:
        return BorderedWindow(rect, inner_factory)

    return factory
