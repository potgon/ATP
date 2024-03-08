from app.evaluation_core.algorithms.tyr import Tyr
from app.evaluation_core.algorithms.frigg import Frigg
from app.trading_data.fetcher import Fetcher


def get_evaluator(fetcher: Fetcher, algo_name):
    if algo_name == "TYR":
        return Tyr(fetcher)
    elif algo_name == "FRIGG":
        return Frigg(fetcher)
    raise Exception("Unknown evaluator algorithm", algo_name)
