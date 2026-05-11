from enum import IntFlag, auto

from game.core.geometry import Vector2


class Directions(IntFlag):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def vector(self):
        x = 0
        y = 0
        if self & Directions.NORTH:
            y -= 1
        if self & Directions.SOUTH:
            y += 1
        if self & Directions.EAST:
            x += 1
        if self & Directions.WEST:
            x -= 1
        return Vector2(x, y)

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self._name_}>"

    def __str__(self):
        return f"{self._name_}"


BaseDirections: set[Directions] = set(Directions)
DirectionsDiagonals: set[Directions] = set(Directions) | {
    Directions.NORTH | Directions.EAST,
    Directions.EAST | Directions.SOUTH,
    Directions.SOUTH | Directions.WEST,
    Directions.WEST | Directions.NORTH,
}

DIRECTION_VECTORS: dict[Directions, Vector2] = {
    d: d.vector() for d in DirectionsDiagonals
}
