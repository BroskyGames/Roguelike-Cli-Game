import esper

from game.core.context import Context
from game.core.geometry.pos import Pos
from game.ecs.components.tags import Compute

COMPUTING_RANGE = 7


class ComputeProcessor(esper.Processor):
    """
    Compute processor finds all entities in range of the player and adds the Compute tag to them, so that they can be processed by other systems.
    """

    def __init__(self, context: Context):
        self._context = context

    def process(self):
        for ent, _ in esper.get_component(Compute):
            esper.remove_component(ent, Compute)

        player_pos = esper.component_for_entity(self._context.player, Pos)
        for dist in range(COMPUTING_RANGE + 1):
            for dx in range(-dist, dist + 1):
                dy = dist - abs(dx)
                for sign in (-1, 1) if dy != 0 else (1,):
                    pos = Pos(player_pos.x + dx, player_pos.y + dy * sign)
                    for ent in self._context.entities_index.get(pos, ()):
                        if not esper.has_component(ent, Compute):
                            esper.add_component(ent, Compute())
