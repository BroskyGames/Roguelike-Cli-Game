import random

from game.game_factory import new_game
from game.map import LevelConfig


def time_all():
    import cProfile
    import pstats

    pr = cProfile.Profile()
    pr.enable()

    rng = random.Random(2515622030321)

    try:
        for _ in range(20):
            seed = rng.randint(0, 2 ** 32 - 1)
            new_game(seed, LevelConfig(30), False, False, True)
    except SystemExit:
        pass

    pr.disable()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(20)


if __name__ == "__main__":
    # game = new_game(2515622030, LevelConfig(30), False, False, True)
    #
    # UI(game).run()
    time_all()
