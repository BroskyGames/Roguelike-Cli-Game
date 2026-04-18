import curses

from game.core.geometry import Pos, Size
from game.ui.curses.basic import Window
from game.ui.rect import WindowRect
from game.ui.views.map_view import MapView


class MapWindow(Window):
    def __init__(self, rect: WindowRect, map_view: MapView, camera_center: Pos):
        super().__init__(rect)
        self.map = map_view
        self.camera_center = camera_center.y, camera_center.x

    def draw(self) -> None:
        self.win.erase()
        h, w = self.win.getmaxyx()
        start_y = self.camera_center[0] - (h // 2)
        start_x = self.camera_center[1] - (w // 4)

        view = self.map.get_view(Pos(start_x, start_y), Size(w // 2, h))

        for y, row in enumerate(view):
            for x, tile in enumerate(row):
                char = str(tile)

                try:
                    self.win.addch(y, x * 2, char)
                except curses.error:
                    # print(screen_y, screen_x, h, w)
                    pass
        self.win.noutrefresh()
