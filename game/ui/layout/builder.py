from game.ui.curses.rect import WindowRect
from game.ui.layout.nodes import LayoutNode


class LayoutBuilder:
    def __init__(self, layout: LayoutNode) -> None:
        self.layout = layout

    def build(self, h: int, w: int) -> dict[str, WindowRect]:
        windows: dict[str, WindowRect] = {}
        self.layout.compute(h, w, 0, 0, windows)
        return windows
