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
        try:
            next(self.processor)
        except StopIteration:
            self.processor = None
            self.working = False

    @abstractmethod
    def make_processor(self) -> Generator[None, None, None]:
        ...


class PlayerTurnManager(StepProcessor):
    def __init__(self, router) -> None:
        super().__init__()
        self.router = router

    def make_processor(self) -> Generator[None, None, None]:
        for ent, (queue, ap, _) in esper.get_components(ActionQueue, ActionPoints, Player):
            while queue.actions:
                if ap.current <= 0:
                    break

                action = queue.actions.popleft()
                self.router.dispatch(action)
                ap.current -= action.base_cost

                yield

            ap.current = ap.max


class EnemyTurnManager(StepProcessor):
    def __init__(self, router) -> None:
        super().__init__()
        self.router = router

    def make_processor(self) -> Generator[None, None, None]:
        for ent, (queue, ap, _) in esper.get_components(ActionQueue, ActionPoints, Player):  # change to AI
            while queue.actions:
                if ap.current <= 0:
                    break

                action = queue.actions.popleft()
                self.router.dispatch(action)
                ap.current -= action.base_cost

                yield

            ap.current = ap.max
