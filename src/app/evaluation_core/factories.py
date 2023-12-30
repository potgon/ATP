from app.evaluation_core.algorithms.tyr import Tyr
from app.trading_data.fetcher import Fetcher

def get_evaluator(fetcher: Fetcher, algo_name):
    if algo_name == "TYR":
        return Tyr(fetcher)
    raise Exception("Unknown evaluator algorithm", algo_name)
