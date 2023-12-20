from django.conf import settings
from tyr.models import Tyr
from trading_data.services.fetcher import Fetcher

def get_evaluator(fetcher: Fetcher):
    if settings.EVALUATOR_VERSION == 'Tyr':
        return Tyr(fetcher)
    else:
        raise Exception("Unknown evaluator algorithm", settings.EVALUATOR_VERSION)