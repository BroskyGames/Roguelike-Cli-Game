from dataclasses import dataclass

import esper

from game.core.context import Context
from game.core.geometry import Pos
from game.core.map_types import Tile
from game.ecs.components.data import Display, FieldOfView, InRoom
from game.ui.rect import Rect


@dataclass
class VisualTile:
    char: str
    dim: bool = False


class MapView:
    def __init__(self, context: Context):
        self._context = context

        room = esper.component_for_entity(self._context.player, InRoom).room
        assert room is not None, "Player not in room on spawn"
        self._cam = self._context.rooms[room].center

    def get_tile(self, y: int, x: int, fov: set[Pos]) -> VisualTile:
        pos = Pos(x, y)

        if pos not in fov:
            if pos in self._context.explored:
                return VisualTile(str(self._context.map.get(pos, Tile())), True)
            return VisualTile(" ", False)

        best = None

        for ent in self._context.entities_index.get(pos, ()):
            disp = esper.try_component(ent, Display)
            if disp and (not best or disp.priority > best.priority):
                best = disp

        if best:
            return VisualTile(best.char)

        return VisualTile(str(self._context.map.get(pos, Tile())))

    def get_view(self, rect: Rect) -> tuple[tuple[VisualTile, ...], ...]:
        fov = self._get_fov()
        return tuple(
            tuple(
                self.get_tile(map_y, map_x, fov)
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

    def _get_fov(self) -> set[Pos]:
        fov = esper.component_for_entity(self._context.player, FieldOfView).visible
        return fov
