import esper

from game.core.context import Context
from game.core.geometry import Pos
from game.ecs.components.data import Trigger
from game.ecs.components.tags import Compute


class TriggerProcessor(esper.Processor):
    def __init__(self, context: Context):
        self._context = context

    def process(self):
        for tid, (trigger, _) in esper.get_components(Trigger, Compute):
            current: set[int] = set()

            for pos in trigger.shape.flatten():
                for ent in self._context.entities_index.get(pos, ()):
                    if not esper.has_components(ent, Pos, Compute):
                        continue

                    current.add(ent)

            entered = current - trigger.occupants
            exited = trigger.occupants - current

            for ent in entered:
                for cb in trigger.on_enter:
                    cb(tid, ent)

            for ent in current:
                for cb in trigger.inside:
                    cb(tid, ent)

            for ent in exited:
                for cb in trigger.on_exit:
                    cb(tid, ent)

            trigger.occupants = current
