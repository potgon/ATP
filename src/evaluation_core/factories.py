from tyr.tyr import Tyr
from trading_data.services.fetcher import Fetcher

def get_evaluator(fetcher: Fetcher, algo_name):
    if algo_name == "TYR":
        return Tyr(fetcher)
    else:
        raise Exception("Unknown evaluator algorithm", algo_name)