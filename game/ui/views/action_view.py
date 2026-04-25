from dataclasses import dataclass

import esper

from game.core.state import State
from game.domain.actions import Action
from game.domain.components.data import ActionQueue


@dataclass(frozen=True, slots=True)
class ActionView:
    repr: str
    cost: float


class ActionQueueView:
    def __init__(self, state: State):
        self._state = state

    def get_action_queue(self) -> tuple[ActionView, ...]:
        queue = esper.component_for_entity(self._state.player, ActionQueue)
        return tuple(self._convert_action(action) for action in queue.actions)

    @staticmethod
    def _convert_action(action: Action) -> ActionView:
        return ActionView(str(action), action.base_cost)
