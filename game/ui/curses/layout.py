from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING

from .rect import WindowRect

if TYPE_CHECKING:
    from .basic import GameWindow

MAX_ROWS = 24
MAX_COLS = 80

LayoutFn = Callable[[int, int], tuple[WindowRect, ...]]
WindowFactory = tuple[type[GameWindow], ...]


@dataclass(slots=True)
class UILayout:
    layout_fn: LayoutFn
    window_types: WindowFactory


def compute_game_layout(rows: int, cols: int) -> tuple[WindowRect, ...]:
    actual_rows = min(rows, MAX_ROWS)
    actual_cols = min(cols, MAX_COLS)

    offset_y = (rows - actual_rows) // 2
    offset_x = (cols - actual_cols) // 2

    log_h = 6
    stat_w = cols // 3
    map_w = cols - stat_w
    map_h = rows - log_h
    stat_h = map_h // 2

    return (
        WindowRect(map_h, map_w, 0 + offset_x, 0 + offset_x),
        WindowRect(stat_h, stat_w, 0 + offset_y, map_w + offset_x),
        WindowRect(map_h - stat_h, stat_w, stat_h + offset_y, map_w + offset_x),
        WindowRect(log_h, cols, map_h + offset_y, 0 + offset_x),
    )


GAME_LAYOUT = UILayout(compute_game_layout, ())  # TODO: Add log, stats, level, map windows
