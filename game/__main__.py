from .logic.map import create_rooms_from_graph
from .logic.graph import assign_tags, generate_graph, print_nodes
from .utils import Pos, display_shape, init_rng

if __name__ == "__main__":
    init_rng()

    start = generate_graph(25, {0: 1.2, 1: 1.1, 2: 1})

    assign_tags(start, .25, .33)

    print_nodes(start)

    rooms = create_rooms_from_graph(start, main_diff=3)

    map: dict[Pos, str] = {}

    for room in rooms.values():
        map |= room.get_shape()

    display_shape(map)