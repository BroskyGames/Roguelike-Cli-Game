from game.game_factory import new_game
from game.interface.debug import display_shape
from game.map.level import LevelConfig

if __name__ == "__main__":
    game = new_game(None, LevelConfig(30), False, True)

    display_shape(game.state.map)