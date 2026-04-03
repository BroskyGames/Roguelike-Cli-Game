from random import Random
from typing import Optional


class GameState:
    def __init__(self, seed: Optional[int] = None):
        self.rng = Random(seed)