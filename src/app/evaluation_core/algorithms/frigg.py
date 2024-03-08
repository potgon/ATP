import pandas as pd

from pmdarima import auto_arima

from app.evaluation_core.base import TradingAlgorithm


class Frigg(TradingAlgorithm):
    def __init__(self, fetcher):
        super().__init__(fetcher)

    def evaluate(self):
        pass

    # fmt: off
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        optimal_model = auto_arima(data, start_p=0, start_q=0, 
                                   max_p=5, max_q=5, m=12, 
                                   start_P=0, seasonal=True, 
                                   d=1, D=1, trace=True, 
                                   error_action="ignore",
                                   suppress_warnings=True, 
                                   stepwise=True)
        
    # fmt: on
    def custom_metric_handler(self, val):
        pass
