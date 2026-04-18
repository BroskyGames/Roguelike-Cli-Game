from game.game_factory import new_game
from game.map.level import LevelConfig
from game.ui.ui import UI

if __name__ == "__main__":
    game = new_game(231232313, LevelConfig(30), False, True)

    # display_shape(game.state.map)

    UI(game).run()
