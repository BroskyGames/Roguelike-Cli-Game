from game.core.core_types import Pos, Size, Vector2
from game.map.room_types import RoomTypes
from game.utils import Reducer

type ASCII = tuple[tuple[str, ...], ...]
ROOM_TEMPLATES: dict[RoomTypes, tuple[ASCII, ...]] = {
    RoomTypes.SPAWN: ((
(" ", " ", " ", "#", "#", "D", "#", "#", " ", " ", " "),
(" ", " ", " ", "#", ".", ".", ".", "#", " ", " ", " "),
(" ", " ", "#", "#", ".", ".", ".", "#", "#", " ", " "),
("#", "#", "#", ".", ".", ".", ".", ".", "#", "#", "#"),
("#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"),
("D", ".", ".", ".", ".", ".", ".", ".", ".", ".", "D"),
("#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"),
("#", "#", "#", ".", ".", ".", ".", ".", "#", "#", "#"),
(" ", " ", "#", "#", ".", ".", ".", "#", "#", " ", " "),
(" ", " ", " ", "#", ".", ".", ".", "#", " ", " ", " "),
(" ", " ", " ", "#", "#", "D", "#", "#", " ", " ", " "),
    ), (
(" ", " ", "#", "#", "D", "#", "#", " ", " "),
(" ", " ", "#", ".", ".", ".", "#", " ", " "),
("#", "#", "#", ".", ".", ".", "#", "#", "#"),
("#", ".", ".", ".", ".", ".", ".", ".", "#"),
("D", ".", ".", ".", ".", ".", ".", ".", "D"),
("#", ".", ".", ".", ".", ".", ".", ".", "#"),
("#", "#", "#", ".", ".", ".", "#", "#", "#"),
(" ", " ", "#", ".", ".", ".", "#", " ", " "),
(" ", " ", "#", "#", "D", "#", "#", " ", " "),
    ), (
(" ", " ", "#", "#", "D", "#", "#", " ", " "),
(" ", "#", "#", ".", ".", ".", "#", "#", " "),
("#", "#", ".", ".", ".", ".", ".", "#", "#"),
("#", ".", ".", ".", ".", ".", ".", ".", "#"),
("D", ".", ".", ".", ".", ".", ".", ".", "D"),
("#", ".", ".", ".", ".", ".", ".", ".", "#"),
("#", "#", " ", ".", ".", ".", ".", "#", "#"),
(" ", "#", "#", ".", ".", ".", "#", "#", " "),
(" ", " ", "#", "#", "D", "#", "#", " ", " "),
    )),
}

def ascii_traverser[T](template: ASCII, reducer: Reducer[T, tuple[Pos, str]], global_pos: Pos = Pos(0, 0)):
    for y in range(len(template)):
        for x in range(len(template[y])):
            reducer((global_pos + Vector2(x, y) + Vector2(-1, -1), template[y][x]))
    return reducer.acc

def accumulate_ascii_doors(data: tuple[Pos, str], acc: tuple[Pos, ...]) -> tuple[Pos, ...]:
    pos, char = data
    return (*acc, pos) if char == 'D' else acc

def get_template_size(template: ASCII) -> Size:
    return Size(len(template[0])-2, len(template)-2)

if __name__ == '__main__':
    print(ascii_traverser(ROOM_TEMPLATES[RoomTypes.SPAWN][2], Reducer(accumulate_ascii_doors, ())))