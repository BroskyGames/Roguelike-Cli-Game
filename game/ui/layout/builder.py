from game.ui.rect import Rect

from .nodes import LayoutNode


class LayoutBuilder:
    def __init__(self, layout: LayoutNode) -> None:
        self.layout = layout

    def build(self, h: int, w: int) -> dict[str, Rect]:
        windows: dict[str, Rect] = {}
        self.layout.compute(h, w, 0, 0, windows)
        return windows
