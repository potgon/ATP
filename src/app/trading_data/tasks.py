from celery import shared_task
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from app.aws_integration.services import send_custom_metric
from app.evaluation_core.factories import get_evaluator
from app.evaluation_core.intervals import AlgorithmInterval
from app.utils.logger import make_log

from .exceptions import DuplicateAssetException
from .fetcher import Fetcher
from .models import Position
from .services import eval_period, instantiate_algo

active_evaluators = {}  # Algo_Name:Evaluator
algo_ticker_pair = {}  # Evaluator:Ticker


def manage_request(algo_name, ticker):
    if ticker in algo_ticker_pair.values():
        raise DuplicateAssetException(ticker)

    if algo_name not in active_evaluators.keys():
        active_evaluators[algo_name] = instantiate_algo(algo_name, ticker)
        algo_ticker_pair[algo_name] = ticker


@shared_task
def schedule_algo(algo_name, broker):
    evaluator = get_evaluator(active_evaluators[algo_name])
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=Algorithm.objects.get(name=algo_name).exec_interval,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.update_or_create(
        name=f"Run Algorithm: {algo_name}",
        defaults={"interval": interval,
                  "task": "app.trading_data.tasks.schedule_algo"},
    )
