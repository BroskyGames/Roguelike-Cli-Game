from typing import Protocol

from ..utils import Pos, Size


class Widget(Protocol):
    pos: Pos
    size: Size
    def render(self, win, game_state) -> None: ...
    def handle_input(self, key) -> None: ...