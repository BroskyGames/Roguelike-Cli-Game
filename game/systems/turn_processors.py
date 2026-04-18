import esper

from game.core.actions import Action, AttackAction, MoveAction
from game.core.geometry import Pos
from game.systems.components import ActionPoints, ActionQueue, IsPlayer


def execute(action: Action) -> None:
    match action:
        case MoveAction(ent, direction, _):
            pos = esper.component_for_entity(ent, Pos)
            new_pos = pos + direction.vector()
            esper.add_component(ent, new_pos)
        case AttackAction(ent, target, _):
            ...


class PlayerTurnProcessor(esper.Processor):
    def process(self) -> None:
        for ent, (queue, ap, _) in esper.get_components(ActionQueue, ActionPoints, IsPlayer):
            if ap.current <= 0 or not queue.actions:
                continue
            action = queue.actions.popleft()
            execute(action)
            ap.current -= action.base_cost
