import random

from .logic.map import create_rooms_from_graph
from .logic.graph import assign_tags, generate_graph, print_nodes
from .utils import display_shape, init_rng

if __name__ == "__main__":
    init_rng(321312)

    start = generate_graph(10, {0: 1.2, 1: 1.1, 2: 1})

    assign_tags(start, .25, .33)

    # print_nodes(start)

    rooms = create_rooms_from_graph(start, main_diff=3)
    display_shape(rooms[5].get_shape())