from enum import Enum, auto
from typing import Callable

import esper

from game.ecs.components.data import Trigger
from game.ecs.components.shape import Shape


class CallbackType(Enum):
    ON_ENTER = auto()
    INSIDE = auto()
    ON_EXIT = auto()


class TriggerManager:
    def __init__(self):
        self.triggers: dict[Shape, int] = {}

    def make_trigger(
        self, shape: Shape, cb_type: CallbackType, callback: Callable[[int, int], None]
    ):
        is_new = shape not in self.triggers
        trigger = (
            esper.component_for_entity(self.triggers[shape], Trigger)
            if not is_new
            else Trigger(shape)
        )

        match cb_type:
            case CallbackType.ON_ENTER:
                trigger.on_enter.append(callback)
            case CallbackType.INSIDE:
                trigger.inside.append(callback)
            case CallbackType.ON_EXIT:
                trigger.on_exit.append(callback)

        if is_new:
            ent = esper.create_entity(trigger)
            self.triggers[shape] = ent

    def add_trigger(self, trigger: Trigger):
        ent = esper.create_entity(trigger)
        self.triggers[trigger.shape] = ent
