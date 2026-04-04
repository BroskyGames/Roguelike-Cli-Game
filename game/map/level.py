from pprint import pprint
from random import Random

from .corridor import build_corridors
from ..interface.debug import display_shape, print_nodes
from ..core.core_types import Pos
from .graph import assign_tags, generate_graph
from .layout import Room, RoomPlacementError, build_rooms_from_graph
from .tile_map import Tile, build_map


def generate_level(
        rng: Random, rooms_amount: int,
        connection_bias: dict[int,float],
        genetic_chance: float, trap_chance: float,
        size_range: tuple[int, int], main_size_increment: int,
        padding_range: tuple[int, int], max_attempts: int, search_radius: int,
        display_debug: bool = False
) -> tuple[list[Room], dict[Pos, Tile]]:
    start = generate_graph(rng, rooms_amount, connection_bias)

    assign_tags(start, rng, genetic_chance, trap_chance)

    if display_debug:
        print_nodes(start)

    while True:
        try:
            rooms = build_rooms_from_graph(start, rng, size_range, main_size_increment, padding_range, max_attempts, search_radius)
            break
        except RoomPlacementError:
            print("Failed to place rooms, retrying...")

    if display_debug:
        pprint(rooms)

    corridors = build_corridors(rooms)

    game_map = build_map(rooms, corridors)

    if display_debug:
        display_shape(game_map)

    return rooms, game_map