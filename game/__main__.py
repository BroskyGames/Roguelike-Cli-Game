import random

from .logic.graph import assign_tags, generate_graph, print_nodes
from .utils import init_rng

if __name__ == "__main__":
    init_rng(321312)

    start = generate_graph(25, {0: 1.2, 1: 1.1, 2: 1})

    assign_tags(start, .25, .33)

    print_nodes(start)
