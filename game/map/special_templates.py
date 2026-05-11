from game.core.geometry.pos import Pos
from game.core.geometry.size import Size
from game.core.geometry.vec import Vector2
from game.core.map_types import RoomTypes
from game.utils import Reducer

# TODO: Add more special rooms
type ASCII = tuple[tuple[str, ...], ...]
ROOM_TEMPLATES: dict[RoomTypes, tuple[ASCII, ...]] = {
    RoomTypes.SPAWN: (
        (
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
        ),
        (
            (" ", " ", "#", "#", "D", "#", "#", " ", " "),
            (" ", " ", "#", ".", ".", ".", "#", " ", " "),
            ("#", "#", "#", ".", ".", ".", "#", "#", "#"),
            ("#", ".", ".", ".", ".", ".", ".", ".", "#"),
            ("D", ".", ".", ".", ".", ".", ".", ".", "D"),
            ("#", ".", ".", ".", ".", ".", ".", ".", "#"),
            ("#", "#", "#", ".", ".", ".", "#", "#", "#"),
            (" ", " ", "#", ".", ".", ".", "#", " ", " "),
            (" ", " ", "#", "#", "D", "#", "#", " ", " "),
        ),
        (
            (" ", " ", "#", "#", "D", "#", "#", " ", " "),
            (" ", "#", "#", ".", ".", ".", "#", "#", " "),
            ("#", "#", ".", ".", ".", ".", ".", "#", "#"),
            ("#", ".", ".", ".", ".", ".", ".", ".", "#"),
            ("D", ".", ".", ".", ".", ".", ".", ".", "D"),
            ("#", ".", ".", ".", ".", ".", ".", ".", "#"),
            ("#", "#", ".", ".", ".", ".", ".", "#", "#"),
            (" ", "#", "#", ".", ".", ".", "#", "#", " "),
            (" ", " ", "#", "#", "D", "#", "#", " ", " "),
        ),
    ),
}


def ascii_traverser[T](
    template: ASCII, reducer: Reducer[T, tuple[Pos, str]], global_pos: Pos = Pos(0, 0)
):
    width = len(template[0])
    height = len(template)
    for y in range(height):
        for x in range(width):
            reducer((global_pos + Vector2(x - 1, y - 1), template[y][x]))
    return reducer.get_acc()


def ascii_border_traverser[T](
    template: ASCII, reducer: Reducer[T, tuple[Pos, str]], global_pos: Pos = Pos(0, 0)
):
    width = len(template[0])
    height = len(template)
    for y in range(height):
        reducer((global_pos + Vector2(-1, y - 1), template[y][0]))
        reducer((global_pos + Vector2(width - 2, y - 1), template[y][width - 1]))
    for x in range(width):
        reducer((global_pos + Vector2(x - 1, -1), template[0][x]))
        reducer((global_pos + Vector2(x - 1, height - 2), template[height - 1][x]))
    return reducer.get_acc()


def acc_ascii_doors(data: tuple[Pos, str], acc: list[Pos]) -> list[Pos]:
    pos, char = data
    if char == "D":
        acc.append(pos)
    return acc


def get_template_size(template: ASCII) -> Size:
    return Size(len(template[0]) - 2, len(template) - 2)


if __name__ == "__main__":
    print(
        ascii_traverser(
            ROOM_TEMPLATES[RoomTypes.SPAWN][2], Reducer(acc_ascii_doors, [])
        )
    )
