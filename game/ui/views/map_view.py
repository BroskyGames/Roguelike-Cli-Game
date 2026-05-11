from dataclasses import dataclass

import esper

from game.core.context import Context
from game.core.geometry import Pos
from game.domain.directions import Directions
from game.domain.map_types import Tile
from game.ecs.components.data import (
    Display,
    DoorState,
    FieldOfView,
    InRoom,
    Memory,
)
from game.ecs.components.tags import Memorable, Player
from game.ui.rect import Rect


@dataclass
class VisualTile:
    char: str
    dim: bool = False


PLAYER_DISPLAY = {
    Directions.NORTH: Display("^", 5),
    Directions.EAST: Display(">", 5),
    Directions.SOUTH: Display("v", 5),
    Directions.WEST: Display("<", 5),
}

DOOR_DISPLAY = {
    DoorState.OPEN: Display(char="+"),
    DoorState.LOCKED: Display(char="X"),
}


class MapView:
    def __init__(self, context: Context):
        self._context = context

        room = esper.component_for_entity(self._context.player, InRoom).room
        assert room is not None, "Player not in room on spawn"
        self._cam = self._context.rooms[room].center

    def get_view(self, rect: Rect) -> tuple[tuple[VisualTile, ...], ...]:
        fov = self._get_fov()
        return tuple(
            tuple(
                self._get_tile(map_y, map_x, fov)
                for map_x in range(rect.x, rect.w + rect.x)
            )
            for map_y in range(rect.y, rect.h + rect.y)
        )

    def get_camera(self) -> tuple[int, int]:
        room = esper.component_for_entity(self._context.player, InRoom).room
        if room is not None:
            self._cam = self._context.rooms[room].center
        else:
            pos = esper.component_for_entity(self._context.player, Pos)
            self._cam = pos

        return self._cam[1], self._cam[0]

    def _get_tile(self, y: int, x: int, fov: frozenset[Pos]) -> VisualTile:
        pos = Pos(x, y)

        if pos not in fov:
            if pos in self._context.explored:
                for ent, mem in esper.get_component(Memory):
                    if mem.pos == pos:
                        return VisualTile(mem.display.char, True)
                return VisualTile(str(self._context.map.get(pos, Tile())), True)
            return VisualTile(" ", False)

        best = None

        for ent in self._context.entities_index.get(pos, ()):
            disp = self._get_display(ent)
            if disp:
                if not best or disp.priority > best[1].priority:
                    best = ent, disp

        if best:
            if esper.has_component(best[0], Memorable):
                esper.add_component(best[0], Memory(pos, best[1]))
            return VisualTile(best[1].char)

        return VisualTile(str(self._context.map.get(pos, Tile())))

    def _get_display(self, ent: int) -> Display | None:
        if door := esper.try_component(ent, DoorState):
            return DOOR_DISPLAY[door]

        if esper.has_component(ent, Player):
            return PLAYER_DISPLAY[esper.component_for_entity(ent, Directions)]

        return esper.try_component(ent, Display)

    def _get_fov(self) -> frozenset[Pos]:
        return esper.component_for_entity(self._context.player, FieldOfView).shape
