from functools import partial

from game.core.map_types import RoomTypes
from game.core.router import Router
from game.ecs.components.data import Trigger
from game.ecs.components.shape import RectShape
from game.map.room import Room


# TODO: write lock_room, is_cleared and unlock_room methods (requires Door entities)
class RoomManager:
    def __init__(self, router: Router):
        self._router = router

    def make_room_triggers(self, room: Room):
        if room.type in (RoomTypes.MAIN, RoomTypes.TRAP):
            trigger = Trigger(RectShape.from_pos_size(room.pos, room.size))
            lock_room = partial(self.lock_room, room)

            trigger.on_enter.append(lambda _, ent: lock_room() if ent == 1 else None)
            self._router.dispatch(trigger)

    def lock_room(self, room: Room):
        print(f"Locking room {room.id}")
