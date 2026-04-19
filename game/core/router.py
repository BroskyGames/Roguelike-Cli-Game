from collections import defaultdict
from typing import Any, Callable

HANDLERS: dict[type, list[Callable[[Any], None]]] = defaultdict(list)


class Router:
    def __init__(self):
        self._handlers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)

    def register[T](self, msg_type: type[T], handler: Callable[[T], None]):
        self._handlers[msg_type].append(handler)

    def dispatch(self, msg: Any):
        for callback in self._handlers[type(msg)]:
            callback(msg)


def handler[T](msg_type: type[T]):
    def wrapper(func: Callable[[T], None]):
        HANDLERS[msg_type].append(func)
        return func

    return wrapper


def register_all_handlers(router: Router):
    for msg_type, fns in HANDLERS.items():
        for fn in fns:
            router.register(msg_type, fn)
