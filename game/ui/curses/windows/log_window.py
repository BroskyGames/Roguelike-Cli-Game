from game.core.logger import Logger
from game.ui.curses.basic import Window
from game.ui.rect import Rect
from game.utils.string import line


class LogWindow(Window):
    def __init__(self, rect: Rect, logger: Logger) -> None:
        super().__init__(rect)
        self.logger = logger

    def draw(self) -> None:
        self.win.erase()
        h, w = self.win.getmaxyx()

        for i, msg in enumerate(self.logger.read(h - 1)):
            self.win.addstr(i, 0, line(f"{i + 1}. {msg}", "", w))

        self.win.noutrefresh()
