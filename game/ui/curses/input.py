import curses

from game.core.geometry import Directions
from game.domain.actions import (
    Action,
    AttackAction,
    ClearQueueAction,
    EndTurnAction,
    MoveAction,
    RemoveLastAction,
)


class InputAdapter:
    def __init__(self, player: int):
        self.player = player
        self.map = {
            ord("w"): lambda: MoveAction(self.player, Directions.NORTH),
            ord("d"): lambda: MoveAction(self.player, Directions.EAST),
            ord("s"): lambda: MoveAction(self.player, Directions.SOUTH),
            ord("a"): lambda: MoveAction(self.player, Directions.WEST),
            ord("f"): lambda: AttackAction(self.player),
            ord(" "): lambda: EndTurnAction(self.player),
            curses.KEY_BACKSPACE: lambda: RemoveLastAction(self.player),
            ord("c"): lambda: ClearQueueAction(self.player),
        }

    def convert(self, key: int) -> Action | None:
        key = self.normalize_key(key)
        factory = self.map.get(key)
        return factory() if factory else None

    @staticmethod
    def normalize_key(key: int) -> int:
        if key in (127, 8):
            return curses.KEY_BACKSPACE
        return key
