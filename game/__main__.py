import random
import sys
from pprint import pprint

from game.game_factory import new_game
from game.map import LevelConfig
from game.ui.ui import UI


def time_all():
    import cProfile
    import pstats

    pr = cProfile.Profile()
    pr.enable()

    rng = random.Random(2515622030321)

    try:
        for _ in range(50):
            seed = rng.randint(0, 2**32 - 1)
            new_game(seed, LevelConfig(30, padding_range=(5, 13)), False, False, True)
    except SystemExit:
        pass

    pr.disable()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(20)


def main():
    game = new_game(2515622030, LevelConfig(30), False, False, True)
    game.start()
    try:
        UI(game).run()
    except SystemExit:
        pprint(game.logger.read(100))

        raise SystemExit


if __name__ == "__main__":
    args = sys.argv[1:]
    time_test = "--time" in args
    if time_test:
        time_all()
    else:
        main()
