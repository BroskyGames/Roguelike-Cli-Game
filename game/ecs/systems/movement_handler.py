import esper

from game.core.context import Context
from game.core.geometry.pos import Pos
from game.domain.actions import MoveAction
from game.domain.directions import DIRECTION_VECTORS
from game.ecs.components.data import InRoom
from game.ecs.components.tags import Collision


class MovementHandler(esper.Processor):
    def __init__(self, context: Context):
        self.context = context

    def process(self, action: MoveAction) -> None:
        pos = esper.component_for_entity(action.ent, Pos)
        new_pos = pos + DIRECTION_VECTORS[action.dir]

        esper.add_component(action.ent, action.dir)

        if not self.validate(action.ent, new_pos):
            return

        esper.add_component(action.ent, new_pos)
        self.context.entities_index[new_pos].add(action.ent)
        self.context.entities_index[pos].remove(action.ent)

        room_id = self.context.map[new_pos].room_id
        room_id = room_id if room_id != -1 else None
        esper.add_component(action.ent, InRoom(room_id))

    def validate(self, action_ent: int, pos: Pos) -> bool:
        if not esper.has_component(action_ent, Collision):
            return True

        if not self.context.map[pos].walkable:
            return False

        for ent in self.context.entities_index[pos]:
            if esper.has_component(ent, Collision):
                return False

        return True
