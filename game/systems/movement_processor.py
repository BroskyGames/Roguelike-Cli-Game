import esper

from game.core.geometry import Pos
from game.core.state import State
from game.domain.actions import MoveAction
from game.domain.components.tags import Obstacle


class MovementProcessor(esper.Processor):
    def __init__(self, state: State):
        self.map = state.map

    def process(self, action: MoveAction) -> None:
        pos = esper.component_for_entity(action.ent, Pos)
        new_pos = pos + action.dir.vector()

        for ent, (ent_pos, _) in esper.get_components(Pos, Obstacle):
            if ent == action.ent:
                continue
            if ent_pos == new_pos:
                return

        if not self.map[new_pos].walkable:
            return

        esper.add_component(action.ent, new_pos)
