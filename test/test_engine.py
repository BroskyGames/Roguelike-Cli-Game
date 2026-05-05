import random

from game.core.engine import Engine
from game.game_factory import new_game
from game.map import LevelConfig


def test_save_load():
    rng = random.Random(43)
    seed = rng.randint(0, 2 ** 32 - 1)

    game = new_game(seed, LevelConfig(10), False, False, False)
    save = Engine(game.get_save())
    assert save == game
    game.rng.randint(0, 5)
    assert save != game
    save.rng.randint(0, 5)
    assert save == game
