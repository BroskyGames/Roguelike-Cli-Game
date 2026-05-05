from random import Random, randint

import esper

from game.core.context import Context
from game.core.engine import Engine
from game.core.geometry import Pos
from game.core.state import State
from game.ecs.components.data import ActionQueue, Display, FieldOfView, InRoom
from game.ecs.components.stats import ActionPoints, FovRange, Health
from game.ecs.components.tags import Collision, Player
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

    context = Context(game_map, rooms)
    spawn_player(context, rooms, 0)
    spawn_enemies(context)

    state = State(context, seed, rng.getstate(), debug)

    return Engine(state)


def spawn_player(context: Context, rooms: tuple[Room, ...], room: int = 0):
    player = spawn_entity(
        context,
        rooms[room].get_center(),
        Player(),
        Display('@', 5),
        Health(20, 20),
        ActionPoints(4, 4),
        FovRange(4),
        InRoom(room),
        ActionQueue(),
        FieldOfView(),
        Collision(),
    )

    context.player = player
    context.last_room = 0


def spawn_entity(context: Context, pos: Pos, *components) -> int:
    ent = esper.create_entity(pos, *components)
    context.entities_index[pos].add(ent)
    return ent


def spawn_enemies(context: Context):
    spawn_entity(
        context,
        Pos(4, 4),
        Display('8'),
        Health(20, 20),
        ActionPoints(4, 4),
        # FovRange(5),
        # FieldOfView(),
        Collision(),
    )
