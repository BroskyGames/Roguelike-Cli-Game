from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Player:
    pass


@dataclass(frozen=True, slots=True)
class Obstacle:
    pass


@dataclass(frozen=True, slots=True)
class Visible:
    pass
