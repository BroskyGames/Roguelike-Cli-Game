from random import Random

from game.map.level import generate_level

if __name__ == "__main__":
    rng = Random()

    rooms, game_map = generate_level(rng, 30,
                 {0: 1.2, 1: 1.1, 2: 1}, .33,
                 .15, (5, 11),
                 3, (5, 8),
                 5, 25, True
             )
