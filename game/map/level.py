from dataclasses import dataclass, field
from pprint import pprint
from random import Random

from game.core.geometry import Pos
from game.core.map_types import Tile
from game.ui.debug import display_shape, print_nodes
from .corridor import build_corridors
from .graph import assign_tags, generate_graph
from .room import Room, build_rooms_from_graph
from .tile_map import build_map


@dataclass(frozen=True)
class LevelConfig:
    rooms_amount: int
    connection_bias: dict[int, float] = field(default_factory=lambda: {0: 1.2, 1: 1.1, 2: 1})
    genetic_chance: float = .33
    trap_chance: float = .15
    size_range: tuple[int, int] = field(default_factory=lambda: (5, 10))
    main_size_increment: int = 2
    padding_range: tuple[int, int] = field(default_factory=lambda: (5, 8))
    max_place_attempts: int = 5
    search_radius: int = 25


def generate_level(
        rng: Random,
        config: LevelConfig,
        display_debug: bool = False,
        display_overlay: bool = False,
) -> tuple[tuple[Room, ...], dict[Pos, Tile]]:
    start = generate_graph(rng, config.rooms_amount, config.connection_bias)

    assign_tags(start, rng, config.genetic_chance, config.trap_chance)

    if display_debug:
        print_nodes(start)

    while True:
        try:
            rooms = build_rooms_from_graph(
                start,
                rng,
                config.size_range,
                config.main_size_increment,
                config.padding_range,
                config.max_place_attempts,
                config.search_radius
            )

            if display_debug:
                pprint(rooms)

            corridors = build_corridors(rooms)
            break
        except RuntimeError as e:
            if display_debug:
                print(f"{e}, retrying...")

    game_map = build_map(rooms, corridors, display_overlay)

    if display_debug:
        display_shape(game_map)

    return tuple(rooms), game_map
