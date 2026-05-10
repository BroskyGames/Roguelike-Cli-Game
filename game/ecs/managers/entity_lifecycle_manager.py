import esper

from game.core.context import Context
from game.core.geometry import Directions, Pos


class EntityLifecycleManager:
    def __init__(self, context: Context):
        self.context = context

    def create(self, pos: Pos, *components) -> int:
        if not any(isinstance(c, Directions) for c in components):
            components = (*components, Directions.NORTH)

        ent = esper.create_entity(pos, *components)
        self.context.entities_index[pos].add(ent)
        return ent

    def destroy(self, ent: int) -> None:
        pos = esper.component_for_entity(ent, Pos)
        self.context.entities_index[pos].discard(ent)
        esper.delete_entity(ent)

    def save(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError
