import curses

from game.core.engine import Engine
from game.core.state import Phase
from .curses.border import bordered
from .curses.input import InputAdapter
from .curses.manager import WindowManager
from .curses.windows.action_window import ActionWindow
from .curses.windows.data_window import DataWindow
from .curses.windows.map_window import MapWindow
from .layout import LayoutBuilder
from .layout.nodes import HSplit, VSplit, WindowNode
from .layout.splits import ClampSplit, FixedSplit, RatioSplit, ReverseSplit, StepSplit
from .views.action_view import ActionQueueView
from .views.data_view import DataView
from .views.map_view import MapView

GameLayout = LayoutBuilder(
    VSplit(
        top=HSplit(
            left=WindowNode("map"),
            right=VSplit(
                top=WindowNode("stats"),
                bottom=WindowNode("actions"),
                split=RatioSplit(1 / 2),
            ),
            split=StepSplit(
                ReverseSplit(ClampSplit(RatioSplit(1 / 4), min_size=24, max_size=48)),
                step=2,
            ),
        ),
        bottom=VSplit(
            top=WindowNode("log"),
            bottom=WindowNode("data"),
            split=ReverseSplit(FixedSplit(1)),
        ),
        split=ReverseSplit(ClampSplit(RatioSplit(1 / 4), min_size=8)),
    )
)


class UI:
    def __init__(self, engine: Engine):
        self._engine = engine
        self._wm: WindowManager | None = None
        self.input_adapter = InputAdapter(self._engine.state.context.player)

    def run(self) -> None:
        curses.wrapper(self._main)

    def _main(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, 244, curses.COLOR_BLACK)
        stdscr.nodelay(True)
        stdscr.keypad(True)
        stdscr.noutrefresh()
        self._wm = WindowManager(
            stdscr,
            GameLayout,
            {
                "map": bordered(
                    lambda r: MapWindow(r, MapView(self._engine.state.context))
                ),
                "actions": bordered(
                    lambda r: ActionWindow(
                        r, ActionQueueView(self._engine.state.context)
                    )
                ),
                "data": lambda r: DataWindow(r, DataView(self._engine.state)),
            },
        )

        self._wm.draw()

        while True:
            key = stdscr.getch()

            if key == curses.KEY_RESIZE:
                self._wm.handle_resize()
            elif key == ord("q"):
                raise SystemExit

            if self._engine.state.phase == Phase.RESOLUTION:
                self._execute_step()
            elif key != -1:
                action = self.input_adapter.convert(key)
                self._engine.handle_actions(action)
                self._wm.draw()

    def _execute_step(self) -> None:
        self._engine.execute_step()
        self._wm.draw()
        curses.napms(250)
