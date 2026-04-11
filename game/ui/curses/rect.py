from __future__ import annotations

from typing import NamedTuple


class WindowRect(NamedTuple):
    lines: int
    cols: int
    y: int
    x: int
