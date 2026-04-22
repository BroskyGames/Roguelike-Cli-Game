from random import Random, randint

import esper

from game.core.engine import Engine
from game.core.state import State
from game.domain.components import ActionPoints, ActionQueue, Display, Health, InRoom, Player, Visible
from game.map import LevelConfig, Room, generate_level


def new_game(
        seed: int | None,
        level_config: LevelConfig,
        display_debug: bool = False,
        display_overlay: bool = False,
        debug: bool = False
) -> Engine:
    if seed is None:
        seed = randint(0, 2 ** 32 - 1)
    rng = Random(seed)

    rooms, game_map = generate_level(rng, level_config, display_debug, display_overlay)

    player = spawn_player(rooms, 0)

    state = State(seed, game_map, rooms, rng_state=rng.getstate(), debug=debug, player=player)

    return Engine(state)


def spawn_player(rooms: tuple[Room, ...], room: int = 0) -> int:
    return esper.create_entity(
        Player(),
        Health(20, 20),
        rooms[room].get_center(),
        ActionPoints(4, 4),
        Display('@'),
        InRoom(room),
        ActionQueue(),
        Visible(),
    )
