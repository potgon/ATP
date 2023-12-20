from celery import shared_task
from .models import Position
from trading_data.services.fetcher import Fetcher
from tyr.tyr import Tyr

@shared_task
def run_tyr():
    pass