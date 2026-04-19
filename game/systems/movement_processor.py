import esper

from game.core.geometry import Pos
from game.core.router import handler
from game.domain.actions import MoveAction


class MovementProcessor(esper.Processor):
    @handler(MoveAction)
    def process(self, action: MoveAction) -> None:
        print("Movement")
        pos = esper.component_for_entity(action.entity, Pos)
        esper.add_component(action.entity, pos + action.direction.vector())
