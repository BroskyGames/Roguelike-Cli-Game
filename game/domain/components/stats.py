from dataclasses import dataclass


@dataclass(slots=True)
class Health:
    health: int
    max_health: int


@dataclass(frozen=True, slots=True)
class Speed:
    speed: int


@dataclass(slots=True)
class ActionPoints:
    current: int
    max: int


@dataclass(frozen=True, slots=True)
class FovRange:
    radius: int
