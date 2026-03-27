from collections import deque
from enum import StrEnum, auto
from typing import Callable, Literal, TYPE_CHECKING, TypeVar, overload
if TYPE_CHECKING:
    from ..logic.graph import RoomNode

T = TypeVar('T')

def bfs(start: "RoomNode", function: Callable[["RoomNode", T], T]) -> T:
    results = None
    queue = deque([start])
    while queue:
        node = queue.popleft()
        results = function(node, results)
        for child in node.children:
            queue.append(child)
    return results
