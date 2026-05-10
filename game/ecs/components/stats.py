from dataclasses import dataclass, field


@dataclass(slots=True)
class Health:
    health: int
    max_health: int


@dataclass(frozen=True, slots=True)
class Speed:
    speed: int


@dataclass(slots=True)
class ActionPoints:
    current: float = field(init=False)
    max: float

    def __post_init__(self):
        self.current = self.max


@dataclass(frozen=True, slots=True)
class FovRange:
    radius: int
