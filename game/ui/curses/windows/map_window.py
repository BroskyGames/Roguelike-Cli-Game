import curses

from game.ui.curses.basic import Window
from game.ui.rect import Rect
from game.ui.views.map_view import MapView


class MapWindow(Window):
    def __init__(self, rect: Rect, map_view: MapView):
        super().__init__(rect)
        self.map_view = map_view

    def draw(self) -> None:
        self.win.erase()
        h, w = self.win.getmaxyx()
        cam = self.map_view.get_camera()
        start_y = cam[0] - (h // 2)
        start_x = cam[1] - (w // 4)

        view = self.map_view.get_view(Rect(h, w // 2, start_y, start_x))

        for y, row in enumerate(view):
            for x, tile in enumerate(row):
                char = str(tile)

                try:
                    self.win.addch(y, x * 2, char)
                except curses.error:
                    # print(screen_y, screen_x, h, w)
                    pass
        self.win.noutrefresh()
