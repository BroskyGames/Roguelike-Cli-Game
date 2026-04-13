from __future__ import annotations

from asyncio import Protocol

from game.ui.curses.rect import WindowRect
from game.ui.layout.splits import SplitSpec


class LayoutNode(Protocol):
    def compute(self, h: int, w: int, y: int, x: int, rects: dict[str, WindowRect]) -> None:
        ...


class WindowNode(LayoutNode):
    def __init__(self, name: str):
        self.name = name

    def compute(self, h, w, y, x, rects):
        rects[self.name] = WindowRect(h, w, y, x)


class HSplit(LayoutNode):
    __slots__ = ("left", "right", "split")

    def __init__(self, left: LayoutNode, right: LayoutNode, split: SplitSpec):
        self.left = left
        self.right = right
        self.split = split

    def compute(self, h, w, y, x, rects):
        left_w, right_w = self.split.compute(w)

        self.left.compute(h, left_w, y, x, rects)
        self.right.compute(h, right_w, y, x + left_w, rects)


class VSplit(LayoutNode):
    __slots__ = ("top", "bottom", "split")

    def __init__(self, top: LayoutNode, bottom: LayoutNode, split: SplitSpec):
        self.top = top
        self.bottom = bottom
        self.split = split

    def compute(self, h, w, y, x, rects):
        top_h, bottom_h = self.split.compute(h)

        self.top.compute(top_h, w, y, x, rects)
        self.bottom.compute(bottom_h, w, y + top_h, x, rects)
