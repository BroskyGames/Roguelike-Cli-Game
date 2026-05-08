from __future__ import annotations

from typing import Protocol


class SplitSpec(Protocol):
    def compute(self, total: int) -> tuple[int, int]: ...


class RatioSplit:
    def __init__(self, ratio: float):
        self.ratio = ratio

    def compute(self, total: int) -> tuple[int, int]:
        a = int(self.ratio * total)
        return a, total - a


class FixedSplit:
    def __init__(self, fixed: int):
        self.fixed = fixed

    def compute(self, total: int) -> tuple[int, int]:
        a = self.fixed
        return a, total - a


class ReverseSplit:
    def __init__(self, split: SplitSpec):
        self.split = split

    def compute(self, total: int) -> tuple[int, int]:
        a, b = self.split.compute(total)
        return b, a


class ClampSplit:
    def __init__(
        self, split: SplitSpec, min_size: int | None = None, max_size: int | None = None
    ):
        self.split = split
        self.min_size = min_size
        self.max_size = max_size

    def compute(self, total: int) -> tuple[int, int]:
        a, _ = self.split.compute(total)
        if self.min_size is not None:
            a = max(a, self.min_size)
        if self.max_size is not None:
            a = min(a, self.max_size)
        return a, total - a


class StepSplit:
    def __init__(self, split: SplitSpec, step: int):
        self.split = split
        self.step = step

    def compute(self, total: int) -> tuple[int, int]:
        a, _ = self.split.compute(total)
        a = (a // self.step) * self.step
        return a, total - a
