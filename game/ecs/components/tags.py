from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Player:
    pass


@dataclass(frozen=True, slots=True)
class Collision:
    pass
