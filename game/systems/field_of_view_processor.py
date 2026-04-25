import math
from fractions import Fraction

import esper

from game.core.context import Context
from game.core.geometry import Pos
from game.domain.components.data import FieldOfView
from game.domain.components.stats import FovRange
from game.domain.components.tags import Moved


class FieldOfViewProcessor(esper.Processor):
    def __init__(self, context: Context):
        self.context = context

    def process(self):
        for ent, (fov, fov_range, pos, _) in esper.get_components(FieldOfView, FovRange, Pos, Moved):
            fov.visible = self._compute_fov(pos, fov_range.radius, ent)

    def _compute_fov(self, origin: Pos, radius: int, ent: int) -> set[Pos]:
        visible: set[Pos] = {origin}

        for quadrant in range(4):
            self._scan_quadrant(visible, origin, radius, quadrant, ent)

        return visible

    def _scan_quadrant(self, visible: set[Pos], origin: Pos, radius: int, quadrant: int, ent: int):
        def transform(row: int, col: int) -> Pos:
            match quadrant:
                case 0:
                    return Pos(origin.x + col, origin.y - row)
                case 1:
                    return Pos(origin.x + row, origin.y + col)
                case 2:
                    return Pos(origin.x + col, origin.y + row)
                case 3:
                    return Pos(origin.x - row, origin.y + col)
            raise ValueError

        def is_blocking(row: int, col: int) -> bool:
            pos = transform(row, col)
            tile = self.context.map.get(pos)
            return tile is None or not tile.transparent

        def reveal(row: int, col: int):
            pos = transform(row, col)
            if pos in self.context.map:
                visible.add(pos)
                if self.context.player == ent:
                    self.context.explored.add(pos)

        def scan(depth: int, start_slope: Fraction, end_slope: Fraction):
            if depth > radius:
                return

            min_col = _round_ties_up(depth * start_slope)
            max_col = _round_ties_down(depth * end_slope)

            prev_blocking = None

            for col in range(min_col, max_col + 1):
                blocking = is_blocking(depth, col)

                if blocking or _is_symmetric(depth, col, start_slope, end_slope):
                    reveal(depth, col)

                if prev_blocking is True and not blocking:
                    start_slope = _slope(depth, col)

                if prev_blocking is False and blocking:
                    new_end = _slope(depth, col)
                    scan(depth + 1, start_slope, new_end)

                prev_blocking = blocking

            if prev_blocking is False:
                scan(depth + 1, start_slope, end_slope)

        scan(1, Fraction(-1), Fraction(1))

    @staticmethod
    def _is_blocking_check():
        pass


def _slope(depth: int, col: int) -> Fraction:
    return Fraction(2 * col - 1, 2 * depth)


def _is_symmetric(depth: int, col: int, start_slope: Fraction, end_slope: Fraction) -> bool:
    return (col >= depth * start_slope) and (col <= depth * end_slope)


def _round_ties_up(n: Fraction) -> int:
    return math.floor(n + Fraction(1, 2))


def _round_ties_down(n: Fraction) -> int:
    return math.ceil(n - Fraction(1, 2))
