from game.game_factory import new_game
from game.map.level import LevelConfig
from game.ui.ui import UI

if __name__ == "__main__":
    game = new_game(None, LevelConfig(30), False, False)

    # display_shape(game.state.map)

    UI(game).run()
