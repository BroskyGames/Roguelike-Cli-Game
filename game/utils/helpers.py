from . import Pos

def display_shape(shape: dict[Pos, str]):
    min_x = min(pos.x for pos in shape)
    min_y = min(pos.y for pos in shape)

    # Find bottom-right corner
    max_x = max(pos.x for pos in shape)
    max_y = max(pos.y for pos in shape)

    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            row += shape.get(Pos(x, y), " ") + ' '
        print(row)