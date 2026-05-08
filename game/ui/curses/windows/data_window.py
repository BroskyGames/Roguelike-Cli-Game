from game.ui.curses.basic import Window
from game.ui.rect import Rect
from game.ui.views.data_view import DataView
from game.utils.string import line


class DataWindow(Window):
    def __init__(self, rect: Rect, data_view: DataView) -> None:
        super().__init__(rect)
        self.data_view = data_view

    def draw(self) -> None:
        self.win.erase()
        _, w = self.win.getmaxyx()
        x, y = self.data_view.get_player_pos()
        self.win.addstr(
            0, 0,
            line(f"Phase: {self.data_view.get_phase()}  Cords: {x}, {y}  {self.data_view.debug_print()}", '', w - 1)
        )

        self.win.noutrefresh()
