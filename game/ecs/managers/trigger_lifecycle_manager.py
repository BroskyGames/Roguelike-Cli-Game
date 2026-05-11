from enum import Enum, auto
from typing import Any, Callable

import esper

from game.core.context import Context
from game.core.geometry.shape import Shape
from game.ecs.components.data import Trigger


class CallbackType(Enum):
    ON_ENTER = auto()
    INSIDE = auto()
    ON_EXIT = auto()


class TriggerLifecycleManager:
    def __init__(self, context: Context):
        self._context = context
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
            self.add_trigger(trigger)

    def add_trigger(self, trigger: Trigger):
        ent = esper.create_entity(trigger)
        self.triggers[trigger.shape] = ent
        for pos in trigger.shape.flatten():
            self._context.entities_index[pos].add(ent)

    def add_component(self, shape: Shape, component):
        if shape not in self.triggers:
            raise ValueError("Shape is not registered as a trigger")
        ent = self.triggers[shape]
        esper.add_component(ent, component)

    def get_component[T](self, shape: Shape, component_type: type[T]) -> T:
        if shape not in self.triggers:
            raise ValueError("Shape is not registered as a trigger")
        ent = self.triggers[shape]
        return esper.component_for_entity(ent, component_type)

    def has_component(self, shape: Shape, component_type: type[Any]) -> bool:
        if shape not in self.triggers:
            raise ValueError("Shape is not registered as a trigger")
        ent = self.triggers[shape]
        return esper.has_component(ent, component_type)
