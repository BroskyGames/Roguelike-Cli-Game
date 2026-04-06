from random import Random, randint

from game.core.engine import GameEngine
from game.core.state import GameState
from game.interface.debug import display_shape
from game.map.level import generate_level

if __name__ == "__main__":
    seed = randint(0, 2**32 - 1)
    rng = Random(seed)

    rooms, game_map = generate_level(rng, 30,
                 {0: 1.2, 1: 1.1, 2: 1}, .33,
                 .15, (5, 10),
                 2, (5, 8),
                 5, 25, False
             )

    state = GameState(seed, rng.getstate(), game_map, True)
    engine = GameEngine(state)

    display_shape(state.map)