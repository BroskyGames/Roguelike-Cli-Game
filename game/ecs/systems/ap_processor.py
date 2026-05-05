import esper

from game.ecs.components.stats import ActionPoints


class ActionPointsProcessor(esper.Processor):
    @staticmethod
    def reset_all():
        for ent, ap in esper.get_component(ActionPoints):
            ap.current = ap.max
