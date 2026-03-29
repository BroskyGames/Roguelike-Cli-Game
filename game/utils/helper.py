from collections import deque
from enum import StrEnum, auto
from typing import Any, Callable, Generic, Literal, ParamSpec, TYPE_CHECKING, TypeVar, TypeVarTuple, Unpack, overload

from .reducers import Reducer

if TYPE_CHECKING:
    from ..logic.graph import RoomNode

def bfs[T](start: "RoomNode", reducer: Reducer[T, "RoomNode"]) -> T:
    queue = deque([start])
    while queue:
        node = queue.popleft()
        reducer(node)
        for child in node.children:
            queue.append(child)
    return reducer.acc