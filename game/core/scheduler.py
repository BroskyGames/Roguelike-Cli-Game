from collections import deque
from typing import Callable

import esper

Task = esper.Processor | Callable


class TaskScheduler:
    def __init__(self):
        self.queue: deque[tuple[Task, bool]] = deque()
        self.current: tuple[Task, bool] | None = None

    def add(self, processor: Task, instant: bool = False) -> None:
        self.queue.append((processor, instant))

    def step(self) -> bool:
        if self.current is None:
            self._next()

        while True:
            if self.current is None:
                return False

            task, instant = self.current

            if instant:
                while True:
                    self._run(task)
                    if self._is_done(task):
                        break
                self._next()
                continue

            self._run(task)

            if self._is_done(task):
                self._next()

            return self.current is not None

    def _next(self) -> None:
        if not self.queue:
            self.current = None
            return

        self.current = self.queue.popleft()
        task, _ = self.current

    @staticmethod
    def _run(item) -> None:
        if hasattr(item, "process"):
            item.process()
        else:
            item()

    @staticmethod
    def _is_done(processor: Task) -> bool:
        return not getattr(processor, "working", False)
