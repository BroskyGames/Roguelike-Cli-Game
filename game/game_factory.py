from random import Random, randint

from game.core.engine import GameEngine
from game.core.state import GameState
from game.map.level import LevelConfig, generate_level


def new_game(seed: int | None, level_config: LevelConfig, display_debug: bool = False, debug: bool = False) -> GameEngine:
    if seed is None:
        seed = randint(0, 2 ** 32 - 1)
    rng = Random(seed)

    rooms, game_map = generate_level(rng, level_config, display_debug)
    state = GameState(seed, rng.getstate(), game_map, debug)
    return GameEngine(state)