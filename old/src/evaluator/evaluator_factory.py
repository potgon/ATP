from typing import Any

from data_processing.fetcher import Fetcher
from evaluator.evaluators.tyr import Tyr
from evaluator.evaluators.ymir import Ymir
from utils.config import EVALUATOR_VERSION


def get_evaluator(fetcher: Fetcher) -> Any:
    if EVALUATOR_VERSION == "Ymir":
        return Ymir(fetcher)
    elif EVALUATOR_VERSION == "Tyr":
        return Tyr(fetcher)
    else:
        raise Exception("Unknown evaluator algorithm", EVALUATOR_VERSION)
