from collections import deque
from enum import StrEnum, auto
from typing import Any, Callable, Generic, Literal, ParamSpec, TYPE_CHECKING, TypeVar, TypeVarTuple, Unpack, overload
if TYPE_CHECKING:
    from ..logic.graph import RoomNode

def bfs[T](start: "RoomNode", function: Callable[["RoomNode", T | None], T], initial: T | None) -> T:
    result = initial
    queue = deque([start])
    while queue:
        node = queue.popleft()
        results = function(node, results)
        for child in node.children:
            queue.append(child)
    return result

T = TypeVar("T")
Ts = TypeVarTuple('Ts')
# TODO: Make T in *functions equivalent to elements of Ts
def combine_reducers(*functions: *tuple[Callable[["RoomNode", T], T]]) -> Callable[["RoomNode", tuple[*Ts]], tuple[*Ts]]:
    def combined(node: "RoomNode", acc: tuple[*Ts]) -> tuple[*Ts]:
        return tuple(
            f(node, acc[i]) for i, f in enumerate(functions)
        )  # type: ignore

    return combined