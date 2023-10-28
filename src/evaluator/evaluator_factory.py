from typing import Callable

from evaluator.evaluators import v1
from utils.config import EVALUATOR_VERSION, RATIO


def get_evaluator() -> Callable:
    match EVALUATOR_VERSION:
        case "v1":
            return v1.evaluate
        case _:
            raise Exception("Unexpected evaluator", EVALUATOR_VERSION)


class Result:
    def __init__(
        self, evaluation: bool, stop_loss: float = 0.0, take_profit: float = 0.0
    ) -> None:
        self.evaluation = evaluation
        self.stop_loss = stop_loss
        self.take_profit = take_profit


def calculate_entry(close: float, ratio=RATIO):
    stop_loss = 1 - RATIO
    take_profit = (RATIO + 1) * close


class Evaluator:
    def __init__(self) -> None:
        self._evaluate = get_evaluator()

    def evaluate(self, data) -> Result:
        evaluation: bool = self._evaluate(data)
        if evaluation:
            stop_loss, take_profit = calculate_entry()
            return Result(
                evaluation=evaluation,
                stop_loss=stop_loss,
                take_profit=take_profit,
            )
        else:
            return Result(evaluation=evaluation)
