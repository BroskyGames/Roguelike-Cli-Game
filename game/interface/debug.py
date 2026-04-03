from game.map.graph import RoomNode
from game.map.map import Tile, TileEnum
from game.core.types import Pos


def display_shape(shape: dict[Pos, Tile]):
    min_x = min(pos.x for pos in shape)
    min_y = min(pos.y for pos in shape)
    max_x = max(pos.x for pos in shape)
    max_y = max(pos.y for pos in shape)

    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            tile = shape.get(Pos(x, y), Tile(TileEnum.EMPTY))
            row += str(tile) + ' '
        print(row)

def print_nodes(node: RoomNode,  prefix="", is_last=True):
    connector = "└─ " if is_last else "├─ "

    print(prefix + connector + f"{node.tag.value}{node.id}")

    new_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(node.children):
        is_last_child = i == len(node.children) - 1
        print_nodes(child, new_prefix, is_last_child)