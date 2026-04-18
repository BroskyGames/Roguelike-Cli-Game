from typing import Callable

from game.ui.curses.basic import Window
from game.ui.rect import Rect


class BorderedWindow(Window):
    def __init__(self, rect: Rect, inner_factory: Callable[[Rect], Window]):
        super().__init__(rect)
        inner_rect = self._inner_rect(rect)
        self._inner = inner_factory(inner_rect)

    @staticmethod
    def _inner_rect(rect: Rect) -> Rect:
        return Rect(rect.h - 2, rect.w - 2, rect.y + 1, rect.x + 1)

    def resize(self, rect: Rect) -> None:
        super().resize(rect)
        self._inner.resize(self._inner_rect(rect))

    def draw(self) -> None:
        self.win.erase()
        self.win.border()
        self.win.noutrefresh()
        self._inner.draw()


def bordered(inner_factory: Callable[[Rect], Window]) -> Callable[[Rect], Window]:
    def factory(rect: Rect) -> BorderedWindow:
        return BorderedWindow(rect, inner_factory)

    return factory
