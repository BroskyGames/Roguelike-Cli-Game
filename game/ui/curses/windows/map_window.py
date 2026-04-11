from game.core.state import GameState
from game.ui.curses.basic import GameWindow


# TODO: Complete MapWindow
class MapWindow(GameWindow):
    def draw(self, state: GameState) -> None:
        raise NotImplementedError("draw")
