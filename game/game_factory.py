from random import Random, randint

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
    debug: bool = False,
) -> Engine:
    if seed is None:
        seed = randint(0, 2**32 - 1)
    rng = Random(seed)

    rooms, game_map = generate_level(rng, level_config, display_debug, display_overlay)

    context = Context(game_map, rooms)

    state = State(context, seed, rng.getstate(), debug)

    engine = Engine(state)

    spawn_player(engine, context, rooms, 0)
    spawn_enemies(engine)

    return engine


def spawn_player(
    engine: Engine, context: Context, rooms: tuple[Room, ...], room: int = 0
):
    player = engine.create_entity(
        rooms[room].center,
        Player(),
        Display("@", 5),
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


def spawn_enemies(engine: Engine):
    engine.create_entity(
        Pos(4, 4),
        Display("8"),
        Health(20, 20),
        ActionPoints(4, 4),
        # FovRange(5),
        # FieldOfView(),
        Collision(),
    )
