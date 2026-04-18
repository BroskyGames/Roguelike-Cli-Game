from random import Random, randint

from game.core.engine import Engine
from game.map.level import LevelConfig, generate_level
from game.state import State


def new_game(seed: int | None, level_config: LevelConfig, display_debug: bool = False, debug: bool = False) -> Engine:
    if seed is None:
        seed = randint(0, 2 ** 32 - 1)
    rng = Random(seed)

    rooms, game_map = generate_level(rng, level_config, display_debug)
    state = State(seed, rng.getstate(), game_map, debug)
    return Engine(state)
