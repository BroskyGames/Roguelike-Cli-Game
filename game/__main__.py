import random

from .ui import main
from .logic.graph import generate_graph, find_longest_path, print_nodes
from .utils import init_rng

if __name__ == "__main__":
    main()
    init_rng(2332 ** random.randint(5, 100))
    spawn = generate_graph(25, {1: 1.3, 2: 1.1, 3: 1})
    main_path = find_longest_path(spawn)
    print_nodes(spawn)