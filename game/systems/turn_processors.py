from abc import ABC, abstractmethod
from typing import Generator

import esper

from game.domain.components import ActionPoints, ActionQueue, Player


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


class PlayerTurnProcessor(StepProcessor):
    def __init__(self, router) -> None:
        super().__init__()
        self.router = router

    def make_processor(self) -> Generator[None, None, None]:
        print("Player turn")
        for ent, (queue, ap, _) in esper.get_components(ActionQueue, ActionPoints, Player):
            if ap.current <= 0 or not queue.actions:
                continue
            action = queue.actions.popleft()
            print(f"Dispatch {action}")
            self.router.dispatch(action)
            yield

            ap.current -= action.base_cost


class EnemyTurnProcessor(StepProcessor):
    def __init__(self, router) -> None:
        super().__init__()
        self.router = router

    def make_processor(self) -> Generator[None, None, None]:
        for ent, (queue, ap, _) in esper.get_components(ActionQueue, ActionPoints, Player):  # change to AI
            if ap.current <= 0 or not queue.actions:
                continue

            action = queue.actions.popleft()
            self.router.dispatch(action)
            ap.current -= action.base_cost

            yield
