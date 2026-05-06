from game.core.geometry import Pos
from game.core.map_types import Tile
from game.map.graph import RoomNode


def display_shape(shape: dict[Pos, Tile]):
    min_x = None
    min_y = None
    max_x = None
    max_y = None

    for pos in shape.keys():
        x = pos.x
        y = pos.y
        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y

    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            tile = shape.get(Pos(x, y), Tile())
            row += str(tile) + ' '
        print(row)


def print_nodes(node: RoomNode, prefix="", is_last=True):
    connector = "└─ " if is_last else "├─ "

    print(prefix + connector + f"{node.type.value}{node.id}")

    new_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(node.children):
        is_last_child = i == len(node.children) - 1
        print_nodes(child, new_prefix, is_last_child)
