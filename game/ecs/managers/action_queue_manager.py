import esper

from game.ecs.components.data import ActionQueue
from game.ecs.components.tags import Player


class ActionQueueManager:
    @staticmethod
    def add(action):
        for ent, (queue, _) in esper.get_components(ActionQueue, Player):
            queue.actions.append(action)

    @staticmethod
    def remove_last():
        for ent, (queue, _) in esper.get_components(ActionQueue, Player):
            if not queue.actions:
                continue
            queue.actions.pop()

    @staticmethod
    def clear():
        for ent, (queue, _) in esper.get_components(ActionQueue, Player):
            queue.actions.clear()
