from random import Random, SystemRandom
from typing import Optional

_rng: Optional[Random] = None

def init_rng(seed: int = None):
    global _rng
    _rng = Random(seed)

def get_rng() -> Random:
    assert _rng is not None, "RNG not initialized. Call init_rng(seed) first."
    return _rng