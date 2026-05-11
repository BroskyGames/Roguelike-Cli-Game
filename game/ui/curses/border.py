from typing import Callable

from game.ui.rect import Rect
from game.utils.string import center

from .basic import Window


class BorderedWindow(Window):
    def __init__(
        self, rect: Rect, inner_factory: Callable[[Rect], Window], title: str = ""
    ) -> None:
        super().__init__(rect)
        inner_rect = self._inner_rect(rect)
        self._inner = inner_factory(inner_rect)
        self.title = title

    @staticmethod
    def _inner_rect(rect: Rect) -> Rect:
        return Rect(rect.h - 2, rect.w - 2, rect.y + 1, rect.x + 1)

    def resize(self, rect: Rect) -> None:
        super().resize(rect)
        self._inner.resize(self._inner_rect(rect))

    def draw(self) -> None:
        self.win.erase()
        self.win.border()

        if self.title:
            _, w = self.win.getmaxyx()
            start_x, title = center(f"{self.title}", w, margin=1)
            self.win.addstr(0, start_x, title)

        self.win.noutrefresh()
        self._inner.draw()


def bordered(
    inner_factory: Callable[[Rect], Window], title: str = ""
) -> Callable[[Rect], Window]:
    def factory(rect: Rect) -> BorderedWindow:
        return BorderedWindow(rect, inner_factory, title)

    return factory
