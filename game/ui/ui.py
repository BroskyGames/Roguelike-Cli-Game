import curses

from game.core.engine import Engine
from .curses.border import bordered
from .curses.manager import WindowManager
from .curses.windows import MapWindow
from .layout import LayoutBuilder
from .layout.nodes import HSplit, VSplit, WindowNode
from .layout.splits import ClampSplit, RatioSplit, ReverseSplit, StepSplit
from .views.map_view import MapView

GameLayout = LayoutBuilder(VSplit(
    top=HSplit(
        left=WindowNode("map"),
        right=VSplit(
            top=WindowNode("stats"),
            bottom=WindowNode("level"),
            split=RatioSplit(1 / 2)
        ),
        split=StepSplit(ReverseSplit(ClampSplit(RatioSplit(1 / 4), min_size=24, max_size=48)), step=2)
    ),
    bottom=WindowNode("log"),
    split=ReverseSplit(ClampSplit(RatioSplit(1 / 4), min_size=8))
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
        stdscr.nodelay(True)
        stdscr.noutrefresh()
        self._wm = WindowManager(stdscr, GameLayout, {
            "map": bordered(lambda r: MapWindow(r, MapView(self._engine.state)))
        })

        self._wm.draw()

        while True:
            key = stdscr.getch()

            if key == curses.KEY_RESIZE:
                self._wm.handle_resize()
            elif key == ord("q"):
                raise SystemExit

            if self._engine.state.phase == "RESOLUTION":
                self._execute_step()
            elif key != -1:
                self._engine.handle_input(key)
                self._wm.draw()

    def _execute_step(self) -> None:
        self._engine.execute_step()
        self._wm.draw()
        curses.napms(150)
