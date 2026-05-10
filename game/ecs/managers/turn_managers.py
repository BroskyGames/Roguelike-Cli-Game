from abc import ABC, abstractmethod
from typing import Generator

import esper

from game.ecs.components.data import ActionQueue
from game.ecs.components.stats import ActionPoints
from game.ecs.components.tags import Player


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


class EnemyTurnManager(StepProcessor):
    def __init__(self, router) -> None:
        super().__init__()
        self.router = router

    def make_processor(self) -> Generator[None, None, None]:
        for _, (queue, ap, _) in esper.get_components(
            ActionQueue, ActionPoints, Player
        ):  # TODO: change to AI
            while queue.actions:
                if ap.current <= 0:
                    break

                action = queue.actions.popleft()
                self.router.dispatch(action)
                ap.current -= action.base_cost

                yield

            ap.current = ap.max
