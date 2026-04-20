import esper

from game.core.geometry import Pos
from game.domain.actions import MoveAction


class MovementProcessor(esper.Processor):
    def process(self, action: MoveAction) -> None:
        pos = esper.component_for_entity(action.ent, Pos)
        esper.add_component(action.ent, pos + action.dir.vector())
