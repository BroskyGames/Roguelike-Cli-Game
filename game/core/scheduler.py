from collections import deque

import esper


class ProcessorScheduler:
    def __init__(self):
        self.queue: deque[esper.Processor] = deque()
        self.current: esper.Processor | None = None

    def add(self, processor: esper.Processor) -> None:
        self.queue.append(processor)

    def start(self) -> None:
        self._next()

    def step(self) -> bool:
        if self.current is None:
            return False

        self.current.process()

        if self._is_done(self.current):
            self._next()

        return self.current is not None

    def _next(self):
        if not self.queue:
            self.current = None
            return

        self.current = self.queue.popleft()

        if hasattr(self.current, "start"):
            self.current.start()

    @staticmethod
    def _is_done(processor: esper.Processor) -> bool:
        return not getattr(processor, "working", False)
