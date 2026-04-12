import curses

from game.core.geometry import Pos
from game.core.map import Tile
from game.ui.curses.basic import Window
from game.ui.curses.rect import WindowRect


# TODO: Complete MapWindow
class MapWindow(Window):
    def __init__(self, rect: WindowRect, map: dict[Pos, Tile], camera_center: Pos):
        super().__init__(rect)
        self.map = map
        self.camera_center = camera_center.y, camera_center.x

    def draw(self) -> None:
        h, w = self.win.getmaxyx()
        start_y = self.camera_center[0] - (h // 2)
        start_x = self.camera_center[1] - (w // 4)
        for screen_y in range(0, h):
            for screen_x in range(0, w, 2):
                map_y = start_y + screen_y
                map_x = start_x + (screen_x // 2)

                tile = self.map.get(Pos(map_x, map_y))

                if tile is None:
                    char = ' '
                else:
                    char = str(tile)

                try:
                    self.win.addch(screen_y, screen_x, char)
                except curses.error:
                    pass
        self.win.border()
