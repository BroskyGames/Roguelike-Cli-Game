from game.game_factory import new_game
from game.map.level import LevelConfig
from game.ui.debug import display_shape

if __name__ == "__main__":
    game = new_game(None, LevelConfig(30), False, True)

    display_shape(game.state.map)
