from celery import shared_task

from .models import Position
from .services import eval_period, instantiate_algo
from .exceptions import DuplicateAssetException
from .fetcher import Fetcher
from app.aws_integration.services import send_custom_metric
from app.evaluation_core.factories import get_evaluator
from app.evaluation_core.intervals import AlgorithmInterval
from app.utils.logger import make_log

active_evaluators = {}
algo_ticker_pair = {}

@shared_task
def manage_algorithm(algo_name, ticker):
    if ticker in algo_ticker_pair.values():
        raise DuplicateAssetException(ticker)
    
    if algo_name not in active_evaluators.keys():
        active_evaluators[algo_name] = instantiate_algo(algo_name, ticker)
        algo_ticker_pair[algo_name] = ticker

    evaluator = active_evaluators[algo_name]
    eval_period(evaluator, algo_name, ticker)
    time.sleep(AlgorithmInterval[algo_name].value)