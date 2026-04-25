from typing import Callable

import esper

from game.core.context import Context
from game.core.geometry import Pos
from game.domain.components.data import FieldOfView
from game.domain.components.stats import FovRange
from game.domain.components.tags import Moved


class FieldOfViewProcessor(esper.Processor):
    def __init__(self, context: Context):
        self.map = context.map

    def process(self):
        for ent, (fov, fov_range, pos, _) in esper.get_components(FieldOfView, FovRange, Pos, Moved):
            print(Pos(1, 1) == Pos(1, 1))
            visible = compute_fov(
                origin=pos,
                radius=5,
                is_blocking=lambda _: False,
            )
            print(len(visible))
            fov.visible = visible

    def is_blocking(self, pos: Pos) -> bool:
        tile = self.map.get(pos)
        if tile is None:
            return False
        return not tile.walkable


def compute_fov(
        origin: Pos,
        radius: int,
        is_blocking: Callable[[Pos], bool],
) -> set[Pos]:
    visible: set[Pos] = set()
    visible.add(origin)

    def cast_light(octant: int, row: int, start_slope, end_slope):
        if start_slope[0] * end_slope[1] < end_slope[0] * start_slope[1]:
            return

        for depth in range(row, radius + 1):
            blocked = False
            new_start = start_slope

            for col in range(depth + 1):
                dx, dy = _transform_octant(octant, col, depth)
                pos = Pos(origin.x + dx, origin.y + dy)

                l_slope = (2 * col - 1, 2 * depth + 1)
                r_slope = (2 * col + 1, 2 * depth - 1)

                if r_slope[0] * start_slope[1] > start_slope[0] * r_slope[1]:
                    continue
                if l_slope[0] * end_slope[1] < end_slope[0] * l_slope[1]:
                    break

                if dx * dx + dy * dy <= radius * radius:
                    visible.add(pos)

                blocking = is_blocking(pos)

                if blocked:
                    if blocking:
                        new_start = r_slope
                    else:
                        blocked = False
                        start_slope = new_start
                else:
                    if blocking and depth < radius:
                        blocked = True
                        cast_light(octant, depth + 1, start_slope, l_slope)
                        new_start = r_slope

            if blocked:
                break

    for octant in range(8):
        cast_light(octant, 1, (1, 1), (0, 1))
    return visible


def _transform_octant(octant: int, x: int, y: int) -> tuple[int, int]:
    if octant == 0: return x, -y
    if octant == 1: return y, -x
    if octant == 2: return y, x
    if octant == 3: return x, y
    if octant == 4: return -x, y
    if octant == 5: return -y, x
    if octant == 6: return -y, -x
    if octant == 7: return -x, -y
    raise ValueError


if __name__ == '__main__':
    visible = compute_fov(
        origin=Pos(0, 0),
        radius=5,
        is_blocking=lambda p: False,
    )

    print(len(visible))
    print(sorted(visible, key=lambda p: (p.x, p.y)))
