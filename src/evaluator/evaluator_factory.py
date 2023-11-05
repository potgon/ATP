from typing import Callable

from evaluator.evaluators import v1, v2
from utils.config import EVALUATOR_VERSION


def get_evaluator() -> Callable:
    match EVALUATOR_VERSION:
        case "v1":
            return v1.evaluate
        case "v2":
            return v2.evaluate
        case _:
            raise Exception("Unexpected evaluator", EVALUATOR_VERSION)
