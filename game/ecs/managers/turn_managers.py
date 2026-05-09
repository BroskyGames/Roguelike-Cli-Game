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

    def start(self) -> None:
        self.processor = self.make_processor()
        self.working = True

    def process(self) -> None:
        assert self.processor is not None, (
            "Processor not started. Call start() before processing."
        )
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
            while queue.actions and ap.current > 0:
                action = queue.actions.popleft()
                self.router.dispatch(action)
                ap.current -= action.base_cost

                if not (queue.actions and ap.current > 0):
                    break

                yield
            ap.current = ap.max


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
