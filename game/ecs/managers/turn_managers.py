from abc import ABC, abstractmethod
from random import Random
from typing import Generator

import esper

from game.core.context import Context
from game.core.logger import Logger
from game.core.router import Router
from game.domain.actions import Action
from game.ecs.components.data import AI, ActionQueue
from game.ecs.components.stats import ActionPoints
from game.ecs.components.tags import Compute, Player
from game.ecs.managers.ai_manager import AIManager
from game.ecs.systems.movement_processor import MovementProcessor


class StepProcessor(esper.Processor, ABC):
    def __init__(self) -> None:
        self.processor = None
        self.working: bool = False

    def process(self) -> None:
        if self.processor is None:
            self.processor = self.make_processor()
            self.working = True
        try:
            next(self.processor)
        except StopIteration:
            self.processor = None
            self.working = False

    @abstractmethod
    def make_processor(self) -> Generator[None, None, None]: ...


class PlayerTurnManager(StepProcessor):
    def __init__(self, router) -> None:
        super().__init__()
        self.router = router

    def make_processor(self) -> Generator[None, None, None]:
        for _, (queue, ap, _) in esper.get_components(
            ActionQueue, ActionPoints, Player
        ):
            while queue.actions:
                action = queue.actions[0]

                if not self.validate(ap.current, action):
                    break

                self.router.dispatch(action)
                ap.current -= action.base_cost
                queue.actions.popleft()

                yield
            ap.current = ap.max

    def validate(self, action_points: float, action: Action) -> bool:
        return action_points >= action.base_cost


class AITurnManager(StepProcessor):
    def __init__(
        self,
        router: Router,
        context: Context,
        rng: Random,
        movement_processor: MovementProcessor,
        logger: Logger,
    ) -> None:
        super().__init__()
        self.router = router
        self.ai_manager = AIManager(context, rng, movement_processor, logger)

    def make_processor(self) -> Generator[None, None, None]:
        for ent, (ap, _, _) in esper.get_components(ActionPoints, AI, Compute):
            while True:
                action = self.ai_manager.process(ent, ap.current)

                if not self.validate(ap.current, action):
                    break

                self.router.dispatch(action)
                ap.current -= action.base_cost

                yield

            ap.current = ap.max

    def validate(self, action_points: float, action: Action) -> bool:
        return action_points >= action.base_cost
