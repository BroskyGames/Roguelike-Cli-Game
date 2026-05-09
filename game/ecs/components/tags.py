from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Player:
    pass


@dataclass(frozen=True, slots=True)
class Enemy:
    pass


@dataclass(frozen=True, slots=True)
class Collision:
    pass


@dataclass(frozen=True, slots=True)
class Memorable:
    pass


@dataclass(frozen=True, slots=True)
class Cleared:
    pass
