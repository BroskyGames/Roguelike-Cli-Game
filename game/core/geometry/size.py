from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Iterator


@dataclass(slots=True, frozen=True)
class Size:
    """w, h must be in [1, 32]"""

    w: int
    h: int
    MASK: ClassVar[int] = (1 << 5) - 1

    def __iter__(self) -> Iterator[int]:
        yield self.w
        yield self.h

    def __hash__(self) -> int:
        return (self.w << 5) | (self.h & self.MASK)
