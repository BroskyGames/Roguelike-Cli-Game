from collections import defaultdict
from typing import Any, Callable


class Router:
    def __init__(self):
        self._handlers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)

    def register[T](self, msg_type: type[T], handler: Callable[[T], None]):
        self._handlers[msg_type].append(handler)

    def dispatch(self, msg: Any):
        assert self._handlers[type(msg)], f"Type not registered in router {type(msg)}"
        for callback in self._handlers[type(msg)]:
            callback(msg)
