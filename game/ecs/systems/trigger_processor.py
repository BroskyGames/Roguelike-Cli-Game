import esper

from game.core.geometry import Pos
from game.ecs.components.data import Trigger


class TriggerProcessor(esper.Processor):
    def process(self):
        movers = {ent: pos for ent, pos in esper.get_component(Pos)}

        for tid, trigger in esper.get_component(Trigger):
            current: set[int] = {
                ent for ent, pos in movers.items() if trigger.shape.contains(pos)
            }

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
