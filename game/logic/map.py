from dataclasses import dataclass, field, InitVar
from pprint import pprint
from typing import List, Tuple, Dict, Optional, Sequence, ClassVar, Self
import random

Pos = Tuple[int, int]

@dataclass(frozen=True)
class RoomTemplate:
    name: Optional[str] = None
    asci_layout: InitVar[Optional[Tuple[str, ...]]] = None
    layout: List[List[str]] = field(default_factory=list)

    registry: ClassVar[Dict[str, "RoomTemplate"]] = {}

    def __post_init__(self, ascii_layout: Optional[Tuple[str, ...]]) -> None:
        # asci => grid
        if ascii_layout:
            col_major = [[ascii_layout[y][x] for y in range(len(ascii_layout))]
                         for x in range(len(ascii_layout[0]))]
            object.__setattr__(self, 'layout', col_major)

        if self.name:
            RoomTemplate.registry[self.name] = self

    def rotate(self, rotation: int) -> Self:
        grid = self.layout
        for _ in range(rotation % 4):
            w, h = len(grid), len(grid[0])
            rotated = [[grid[x][h - 1 - y] for x in range(w)] for y in range(h)]
            grid = rotated
        return RoomTemplate(layout=grid)

    def display(self):
        for y in range(len(self.layout[0])):
            for x in range(len(self.layout)):
                print(self.layout[x][y], end=" ")
            print()

RoomTemplate(
    "square", (
        "##D##",
        "#...#",
        "D...D",
        "#...#",
        "##D##",
    ))
RoomTemplate(
    "rectangle", (
        "##D##",
        "#...#",
        "#...#",
        "D...D",
        "#...#",
        "#...#",
        "##D##",
    )
)
RoomTemplate(
    "L-shape", (
        "##D##    ",
        "#...#    ",
        "#...#    ",
        "#...#    ",
        "#...#####",
        "#.......#",
        "#.......D",
        "#.......#",
        "####D####",
    )
)

@dataclass
class Room:
    pos: Pos
    template: str
    rotate: int = 0
    min_doors: int = 1
    door_probability: float = 0.5

    shape: List[List[str]] = field(default_factory=list)
    doors: List[Pos] = field(default_factory=list)

    def __post_init__(self):
        self.shape = RoomTemplate.registry[self.template].rotate(self.rotate).layout
        self._resolve_doors()

    def _resolve_doors(self):
        # Find prop doors in template
        prop = []
        for y, row in enumerate(self.shape):
            for x, char in enumerate(row):
                if char == "D":
                    prop.append((x, y))
        # Resolve found doors
        random.shuffle(prop)
        while prop:
            x, y = prop.pop(0)
            if random.random() < self.door_probability or self.min_doors - len(self.doors) == len(prop) + 1:
                self.doors.append((x, y))
                self.shape[y][x] = '+'
            else:
                self.shape[y][x] = '#'

    @property
    def width(self) -> int:
        return len(self.shape[0])

    @property
    def height(self) -> int:
        return len(self.shape)

# Not tested

from collections import deque

@dataclass
class Corridor:
    start: Pos
    end: Pos
    grid: List[List[str]]  # reference to dungeon map
    path: List[Pos] = field(default_factory=list)

    def __post_init__(self):
        self.path = self._find_path()
        self._carve()

    def _neighbors(self, x: int, y: int) -> List[Pos]:
        # deterministic order (important!)
        return [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

    def _is_walkable(self, x: int, y: int) -> bool:
        if y < 0 or y >= len(self.grid):
            return False
        if x < 0 or x >= len(self.grid[0]):
            return False
        return self.grid[y][x] in (' ', '.', '+')  # allow empty + doors

    def _find_path(self) -> List[Pos]:
        queue = deque([self.start])
        came_from: Dict[Pos, Optional[Pos]] = {self.start: None}

        while queue:
            current = queue.popleft()

            if current == self.end:
                break

            for nx, ny in self._neighbors(*current):
                if (nx, ny) not in came_from and self._is_walkable(nx, ny):
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))

        # reconstruct path
        if self.end not in came_from:
            return []  # no valid path

        path = []
        cur = self.end
        while cur:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        return path

    def _carve(self):
        for x, y in self.path:
            if self.grid[y][x] == ' ':
                self.grid[y][x] = '.'


if __name__ == '__main__':
    RoomTemplate.registry["square"].rotate(2).display()
