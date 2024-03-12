from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error

from app.evaluation_core.model_base import ModelTrainer


class ARIMATrainer(ModelTrainer):
    def __init__(self, order, seasonal_order=None, auto_arima_enabled=False):
        super().__init__()
        self.order = order
        self.seasonal_order = seasonal_order
        self.auto_arima_enabled = auto_arima_enabled
        self.trained_model = None

    def train(self, data):
        if self.auto_arima_enabled:
            # fmt: off
            self.trained_model = auto_arima(data, start_p=1, start_q=1,
                                            max_p=5, max_q=5, m=12,
                                            seasonal=True, trace=True,
                                            error_action='ignore',  
                                            suppress_warnings=True, 
                                            stepwise=True)
            # fmt: on
        else:
            model = ARIMA(data, order=self.order, seasonal_order=self.seasonal_order)
            self.trained_model = model.fit()

    def evaluate(self, actual, forecasted):
        return mean_absolute_error(actual, forecasted)

    def predict(self, steps):
        return self.trained_model.forecast(steps=steps)
