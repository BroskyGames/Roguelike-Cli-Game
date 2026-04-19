import esper

from game.domain.components import ActionPoints


class ActionPointsProcessor(esper.Processor):
    @staticmethod
    def reset_all():
        for ent, ap in esper.get_component(ActionPoints):
            ap.current = ap.max
