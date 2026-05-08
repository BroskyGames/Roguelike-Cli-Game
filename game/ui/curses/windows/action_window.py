import curses

from game.ui.curses.basic import Window
from game.ui.rect import Rect
from game.ui.views.action_view import ActionQueueView
from game.utils.string import line


class ActionWindow(Window):
    def __init__(self, rect: Rect, action_view: ActionQueueView) -> None:
        super().__init__(rect)
        self.action_view = action_view

    def draw(self) -> None:
        self.win.erase()
        h, w = self.win.getmaxyx()
        self.win.addstr(0, 0, "Action Queue".center(w))
        for i, action in enumerate(self.action_view.get_action_queue()[:h]):
            try:
                self.win.addstr(
                    i + 2, 0, line(f"{i + 1}. {action.repr}", f"-{action.cost}", w)
                )
            except curses.error:
                pass
        self.win.noutrefresh()
