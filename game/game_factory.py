from random import Random, randint

import esper

from game.core.engine import Engine
from game.core.state import State
from game.map.level import LevelConfig, generate_level
from game.systems.turn_processors import PlayerTurnProcessor


def new_game(seed: int | None, level_config: LevelConfig, display_debug: bool = False, debug: bool = False) -> Engine:
    if seed is None:
        seed = randint(0, 2 ** 32 - 1)
    rng = Random(seed)

    rooms, game_map = generate_level(rng, level_config, display_debug)
    state = State(seed, game_map, tuple(rooms), rng_state=rng.getstate(), debug=debug)
    return Engine(state)


def processor_setup():
    esper.add_processor(PlayerTurnProcessor(), priority=10)
