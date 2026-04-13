import curses

from game.core.engine import Engine
from game.ui.curses.border import bordered
from game.ui.curses.manager import WindowManager
from game.ui.curses.windows.map_window import MapWindow
from game.ui.layout import HSplit, LayoutBuilder, SplitSpec, VSplit, WindowNode

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
        stdscr.noutrefresh()
        self._wm = WindowManager(stdscr, GameLayout, {
            "map": bordered(lambda r: MapWindow(r, self._engine.state.map, self._engine.state.camera_center))
        })

        self._wm.draw()

        while True:
            key = stdscr.getch()

            if key == curses.KEY_RESIZE:
                self._wm.handle_resize()
            elif key == ord("q"):
                break
            else:
                self._engine.handle_input(key)
                self._wm.draw()
