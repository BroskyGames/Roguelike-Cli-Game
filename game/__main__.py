from random import Random, randint

from game.map.level import generate_level

if __name__ == "__main__":
    seed = randint(0, 2**32 - 1)
    print(f"Seed: {seed}")
    rng = Random(seed)

    rooms, game_map = generate_level(rng, 30,
                 {0: 1.2, 1: 1.1, 2: 1}, .33,
                 .15, (5, 10),
                 2, (5, 8),
                 5, 25, True
             )
