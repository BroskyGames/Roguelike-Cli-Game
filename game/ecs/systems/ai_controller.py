from collections import deque
from random import Random
from typing import Callable

import esper

from game.core.context import Context
from game.core.geometry import (
    Pos,
    Vector2,
    manhattan,
)
from game.core.logger import Logger
from game.domain.actions import Action, AttackAction, MoveAction, WaitAction
from game.domain.directions import DIRECTION_VECTORS, BaseDirections, Directions
from game.ecs.components.data import AI, AIType, FieldOfView
from game.ecs.systems.movement_handler import MovementHandler

type ValidateFn = Callable[[int, Pos], bool]


class AIController:
    def __init__(
        self,
        context: Context,
        rng: Random,
        movement_processor: MovementHandler,
        logger: Logger,
    ) -> None:
        self._context = context
        self.rng = rng
        self.move_validator = movement_processor.validate
        self.logger = logger

    def process(self, ent: int, action_points: float) -> Action:
        assert esper.has_component(ent, AI), f"Entity {ent} shouldn't be handled by AI"
        assert esper.has_components(ent, FieldOfView, Pos, Directions)

        ai = esper.component_for_entity(ent, AI).type

        pos = esper.component_for_entity(ent, Pos)
        fov = esper.component_for_entity(ent, FieldOfView)
        facing = esper.component_for_entity(ent, Directions)

        match ai:
            case AIType.BASIC:
                return self.aggressive_ai(ent, action_points, pos, fov, facing)

    def basic_ai(
        self,
        ent: int,
        action_points: float,
        pos: Pos,
        fov: FieldOfView,
        facing: Directions,
    ) -> Action:
        player_pos = esper.component_for_entity(self._context.player, Pos)
        attack_pos = pos + DIRECTION_VECTORS[facing]
        adjacent = any(player_pos == pos + DIRECTION_VECTORS[d] for d in BaseDirections)

        if player_pos == attack_pos and action_points >= AttackAction.base_cost:
            return AttackAction(ent)
        elif adjacent:
            return MoveAction(ent, _to_base_direction(player_pos - pos))

        if fov.contains(player_pos):
            self.logger.add(
                f"Manhattan: {manhattan(pos, player_pos)}, ap: {action_points}"
            )
            if (
                manhattan(pos, player_pos) == 2
                and action_points < AttackAction.base_cost + MoveAction.base_cost
                and (pos.x == player_pos.x or pos.y == player_pos.y)
            ):
                WaitAction(ent)
            if action := _try_move_to(ent, pos, player_pos - pos, self.move_validator):
                return action

        # if self.rng.random() > 0.2:
        #     if action := _try_wander(ent, pos, self.rng, self.validator):
        #         return action

        return WaitAction(ent)

    def aggressive_ai(
        self,
        ent: int,
        action_points: float,
        pos: Pos,
        fov: FieldOfView,
        facing: Directions,
    ):
        player_pos = esper.component_for_entity(self._context.player, Pos)
        attack_pos = pos + DIRECTION_VECTORS[facing]
        adjacent = any(player_pos == pos + DIRECTION_VECTORS[d] for d in BaseDirections)

        if player_pos == attack_pos and action_points >= AttackAction.base_cost:
            return AttackAction(ent)
        elif adjacent:
            return MoveAction(ent, _to_base_direction(player_pos - pos))

        if fov.contains(player_pos):
            if action := _try_move_to(ent, pos, player_pos - pos, self.move_validator):
                return action

        # if self.rng.random() > 0.2:
        #     if action := _try_wander(ent, pos, self.rng, self.validator):
        #         return action

        return WaitAction(ent)


def _try_move_to(
    ent: int, pos: Pos, preferred: Vector2, validate: ValidateFn
) -> MoveAction | None:
    direction = _find_valid_direction(ent, pos, _to_base_direction(preferred), validate)

    if direction is not None:
        return MoveAction(ent, direction)


def _try_wander(
    ent: int, pos: Pos, rng: Random, validate: ValidateFn
) -> MoveAction | None:
    directions = list(BaseDirections)
    rng.shuffle(directions)

    for direction in directions:
        new_pos = pos + DIRECTION_VECTORS[direction]

        if validate(ent, new_pos):
            return MoveAction(ent, direction)


def _to_base_direction(vec: Vector2) -> Directions:
    x = vec.x
    y = vec.y

    if abs(x) <= abs(y):
        if y > 0:
            return Directions.SOUTH
        return Directions.NORTH
    if x > 0:
        return Directions.EAST
    return Directions.WEST


def _find_valid_direction(
    ent: int, pos: Pos, preferred: Directions, validate: ValidateFn
) -> Directions | None:
    directions = _get_ordered_directions(preferred)

    for direction in directions:
        new_pos = pos + DIRECTION_VECTORS[direction]

        if validate(ent, new_pos):
            return direction

    return None


def _get_ordered_directions(preferred: Directions):
    directions = deque(sorted(BaseDirections))

    while directions[0] != preferred:
        directions.rotate()

    return list(directions)
