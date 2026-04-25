from dataclasses import dataclass

import esper

from game.core.context import Context
from game.domain.actions import Action
from game.domain.components.data import ActionQueue


@dataclass(frozen=True, slots=True)
class ActionView:
    repr: str
    cost: float


class ActionQueueView:
    def __init__(self, context: Context):
        self._context = context

    def get_action_queue(self) -> tuple[ActionView, ...]:
        queue = esper.component_for_entity(self._context.player, ActionQueue)
        return tuple(self._convert_action(action) for action in queue.actions)

    @staticmethod
    def _convert_action(action: Action) -> ActionView:
        return ActionView(action.str(True), action.base_cost)
