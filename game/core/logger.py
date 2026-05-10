from collections import deque
from typing import Deque, Tuple


class Logger:
    def __init__(self, max_size: int = 50) -> None:
        self._log: Deque[str] = deque(maxlen=max_size)

    def add(self, msg: str) -> None:
        self._log.append(msg)

    def read(self, n: int) -> Tuple[str, ...]:
        if n <= 0:
            return ()

        # return last n entries
        if n >= len(self._log):
            return tuple(self._log)

        return tuple(list(self._log)[-n:])
