import pandas as pd

from pmdarima import auto_arima

from app.evaluation_core.base import TradingAlgorithm


class Frigg(TradingAlgorithm):
    def __init__(self, fetcher):
        super().__init__(fetcher)

    def evaluate(self):
        pass

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def custom_metric_handler(self, val):
        pass
