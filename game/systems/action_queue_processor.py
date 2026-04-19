import esper

from game.domain.components import ActionQueue, Player


class ActionQueueProcessor(esper.Processor):
    @staticmethod
    def add(action):
        print(f"Added action to queue {action}")
        for ent, (queue, _) in esper.get_components(ActionQueue, Player):
            queue.actions.append(action)

    @staticmethod
    def remove_last():
        for ent, (queue, _) in esper.get_components(ActionQueue, Player):
            queue.actions.pop()

    @staticmethod
    def clear():
        for ent, (queue, _) in esper.get_components(ActionQueue, Player):
            queue.actions.clear()
