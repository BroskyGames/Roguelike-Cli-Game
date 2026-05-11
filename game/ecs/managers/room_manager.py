from typing import cast

import esper

from game.core.context import Context
from game.core.geometry import Pos
from game.core.map_types import RoomTypes
from game.ecs.components.data import Doors, DoorState, InRoom
from game.ecs.components.shape import RectShape, Shape
from game.ecs.components.tags import Cleared, Collision, Enemy, Memorable
from game.ecs.managers.entity_lifecycle_manager import EntityLifecycleManager
from game.ecs.managers.trigger_lifecycle_manager import (
    CallbackType,
    TriggerLifecycleManager,
)
from game.map.room import Room


class RoomManager:
    def __init__(
        self,
        context: Context,
        trigger_manager: TriggerLifecycleManager,
        entity_manager: EntityLifecycleManager,
    ):
        self._context = context
        self._trigger_manager = trigger_manager
        self._entity_manager = entity_manager
        self._rooms: dict[int, Shape] = {}

    # --- API ---

    def init_rooms(self):
        for room in self._context.rooms:
            self.make_room_triggers(room)

    def make_room_triggers(self, room: Room):
        if room.type in (RoomTypes.MAIN, RoomTypes.TRAP):
            shape = self._rooms.setdefault(
                room.id, RectShape.from_pos_size(room.pos, room.size)
            )

            self._trigger_manager.make_trigger(
                shape,
                CallbackType.ON_ENTER,
                self.trap_room_on_enter,
            )
            self._trigger_manager.make_trigger(
                shape,
                CallbackType.INSIDE,
                self.trap_room_inside,
            )
            self._trigger_manager.add_component(shape, InRoom(room.id))

            self.create_doors(room)

    # --- Logic ---

    def trap_room_on_enter(self, room_ent: int, ent: int):
        room_id = cast(int, esper.component_for_entity(room_ent, InRoom).room)
        if ent == self._context.player and not self._trigger_manager.has_component(
            self._rooms[room_id], Cleared
        ):
            room = self._context.rooms[room_id]
            self.lock_room(room)

    def trap_room_inside(self, room_ent: int, _: int):
        room_id = cast(int, esper.component_for_entity(room_ent, InRoom).room)
        if self.is_cleared(room_id) and not esper.has_component(room_ent, Cleared):
            room = self._context.rooms[room_id]
            self.unlock_room(room)
            self._trigger_manager.add_component(self._rooms[room_id], Cleared())

    # --- Helpers ---
    def is_cleared(self, room_id: int) -> bool:
        for _, (pos, _) in esper.get_components(Pos, Enemy):
            if self._rooms[room_id].contains(pos):
                return False
        return True

    def lock_room(self, room: Room):
        for door_id in self._trigger_manager.get_component(
            self._rooms[room.id], Doors
        ).doors:
            esper.add_component(door_id, DoorState.LOCKED)
            esper.add_component(door_id, Collision())

    def unlock_room(self, room: Room):
        for door_id in self._trigger_manager.get_component(
            self._rooms[room.id], Doors
        ).doors:
            esper.add_component(door_id, DoorState.OPEN)
            esper.remove_component(door_id, Collision)

    def create_doors(self, room: Room):
        doors = set()
        for door in room.doors:
            door_id = self._entity_manager.create(door.pos, DoorState.OPEN, Memorable())
            doors.add(door_id)

        self._trigger_manager.add_component(
            self._rooms[room.id], Doors(frozenset(doors))
        )
