import curses

from game.core.engine import Engine
from game.ui.curses.layout import HSplit, LayoutBuilder, SplitSpec, VSplit, WindowNode
from game.ui.curses.manager import WindowManager
from game.ui.curses.windows.map_window import MapWindow

GameLayout = LayoutBuilder(VSplit(
    top=HSplit(
        left=WindowNode("map"),
        right=VSplit(
            top=WindowNode("stats"),
            bottom=WindowNode("level"),
            split=SplitSpec(ratio=0.5)
        ),
        split=SplitSpec(ratio=3 / 4)
    ),
    bottom=WindowNode("log"),
    split=SplitSpec(fixed=8, reverse=True)
))


class UI:
    def __init__(self, engine: Engine):
        self._engine = engine
        self._wm: WindowManager | None = None

    def run(self) -> None:
        curses.wrapper(self._main)

    def _main(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        curses.start_color()
        self._wm = WindowManager(stdscr, GameLayout, {
            "map": lambda r: MapWindow(r, self._engine.state.map, self._engine.state.camera_center)
        })

        while True:
            self._wm.draw()
            key = stdscr.getch()

            if key == curses.KEY_RESIZE:
                self._wm.handle_resize()
            elif key == ord("q"):
                break
            else:
                self._engine.handle_input(key)
