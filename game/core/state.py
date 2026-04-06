from random import Random, randint
from typing import Optional


class GameState:
    __slots__ = ["rng", "seed", "map"]
    def __init__(self, seed: Optional[int] = None, debug: bool = False):
        if seed is None:
            seed = randint(0, 2**32 - 1)
        self.seed = seed
        if debug:
            print(f"Seed: {seed}")
        self.rng = Random(seed)
