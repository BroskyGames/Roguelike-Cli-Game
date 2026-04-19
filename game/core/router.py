from collections import defaultdict
from typing import Any, Callable


class Router:
    def __init__(self):
        self._handlers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)

    def register[T](self, msg_type: type[T], handler: Callable[[T], None]):
        self._handlers[msg_type].append(handler)

    def dispatch(self, msg: Any):
        for handler in self._handlers[type(msg)]:
            handler(msg)

    def handler[T](self, msg_type: type[T]):
        def wrapper(func: Callable[[T], None]):
            self.register(msg_type, func)
            return func

        return wrapper
