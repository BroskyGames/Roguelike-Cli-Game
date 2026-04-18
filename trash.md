# Mutable_Pos

```python
@runtime_checkable
class IsPosition(Protocol):
    @property
    def x(self) -> int: ...

    @property
    def y(self) -> int: ...


class PositionOps(ABC):
    def __add__(self: Self, other: "Vector2") -> Self:
        if isinstance(other, Vector2):
            return self.__class__(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self: Self, other: IsPosition) -> "Vector2":
        if isinstance(other, IsPosition):
            return Vector2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __iter__(self: Self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __getitem__(self: Self, index: int) -> int:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError


@dataclass(slots=True, frozen=True)
class Pos(PositionOps):
    x: int
    y: int


@dataclass(slots=True)
class MutablePos(PositionOps):
    x: int
    y: int

    def __iadd__(self: "MutablePos", other: IsPosition) -> "MutablePos":
        self.x += other.x
        self.y += other.y
        return self
```

# Rooms

```python
class Room:
    def __init__(self, pos: Pos, template: str, rotate: int = 0, min_doors: int = 1, door_chance: float = 0.5) -> None:
        self.pos: Pos = pos
        self.template: str = template
        self.rotate: int = rotate
        self.min_doors: int = min_doors
        self.door_chance: float = door_chance

        self.shape: List[List[str]] = RoomTemplate.registry[self.template].rotate(self.rotate).layout
        self.doors: List[Pos] = []
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
            if random.random() < self.door_chance or self.min_doors - len(self.doors) == len(prop) + 1:
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
```

# Templates

```python
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
```

# Corridors

```python
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
```

# Curses Example

```python
def cursor_movement(k: int, cx: int, cy: int, w: int, h: int) -> tuple[int, int]:
    if k == curses.KEY_DOWN:
        cy = min(h - 1, cy + 1)
    elif k == curses.KEY_UP:
        cy = max(0, cy - 1)
    elif k == curses.KEY_RIGHT:
        cx = min(w - 1, cx + 1)
    elif k == curses.KEY_LEFT:
        cx = max(0, cx - 1)

    return cx, cy


def center_x_str(string: str, width: int) -> int:
    return (width // 2) - (len(string) // 2)


def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Reset Canvas
    stdscr.clear()
    stdscr.refresh()

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while k != ord('q'):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        cursor_x, cursor_y = cursor_movement(k, cursor_x, cursor_y, width, height)

        # Strings
        title = "Curses example"[:width - 1]
        subtitle = "Written by Clay McLeod"[:width - 1]
        keystr = "Last key pressed: {}".format(k)[:width - 1]
        statusbarstr = f"Press 'q' to exit | STATUS BAR | Pos: {cursor_x}, {cursor_y}"[:width - 1]
        if k == 0:
            keystr = "No key press detected..."[:width - 1]
        start_y = (height // 2) - 3

        # Rendering some text
        whstr = f"Width: {width}, Height: {height}"
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        stdscr.addstr(start_y, center_x_str(title, width), title, curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(start_y + 1, center_x_str(subtitle, width), subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, center_x_str(keystr, width), keystr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu)
```