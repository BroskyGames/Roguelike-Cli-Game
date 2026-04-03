from random import Random

from game.map.level import generate_level

# TODO: Complete RNG argument distribution
if __name__ == "__main__":
    rng = Random()

    rooms, game_map = generate_level(rng, 30,
                 {0: 1.2, 1: 1.1, 2: 1}, .25,
                 .15, (6, 12),
                 3, (5, 8),
                 5, 25, True
             )
