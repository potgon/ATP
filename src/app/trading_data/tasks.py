from celery import shared_task

from .models import Position
from .services import eval_period, instantiate_algo
from .exceptions import DuplicateAssetException
from aws_integration.services import send_custom_metric
from evaluation_core.factories import get_evaluator
from evaluation_core.intervals import AlgorithmInterval
from fetcher import Fetcher
from utils.logger import make_log, log_full_dataframe

operative_algos = {}
active_assets = {}

@shared_task
def manage_algorithm(algo_name, ticker):
    if ticker in active_assets:
        raise DuplicateAssetException(ticker)
    
    if algo_name not in operative_algos:
        evaluator = instantiate_algo(algo_name, ticker)
        operative_algos[algo_name] = evaluator

    active_assets[ticker] = algo_name
    evaluator = operative_algos[algo_name]
    eval_period(evaluator, algo_name, ticker)
    time.sleep(AlgorithmInterval[algo_name].value)