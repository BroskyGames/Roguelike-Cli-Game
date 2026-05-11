import esper

from game.ecs.components.data import ActionQueue


class PlayerActionQueueService:
    def __init__(self, player: int) -> None:
        self.player = player

    def add(self, action):
        queue = esper.component_for_entity(self.player, ActionQueue)
        queue.actions.append(action)

    def remove_last(self):
        queue = esper.component_for_entity(self.player, ActionQueue)
        if not queue.actions:
            return
        queue.actions.pop()

    def clear(self):
        queue = esper.component_for_entity(self.player, ActionQueue)
        queue.actions.clear()
