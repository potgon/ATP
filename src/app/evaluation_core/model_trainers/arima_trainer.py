from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error

from app.evaluation_core.model_base import ModelTrainer


class ARIMATrainer(ModelTrainer):
    def __init__(self, order=None, seasonal_order=None, auto_arima_enabled=False):
        super().__init__()
        self.auto_arima_enabled = auto_arima_enabled
        if not self.auto_arima_enabled:
            self.order = order
            self.seasonal_order = seasonal_order
        else:
            self.order = None
            self.seasonal_order = None
        self.trained_model = None

    def train(self, data):
        if self.auto_arima_enabled:
            # fmt: off
            auto_model = auto_arima(data, start_p=1, start_q=1,
                                    max_p=5, max_q=5, m=12,
                                    start_P=0, seasonal=True, D=1, trace=True,
                                    error_action='ignore',  
                                    suppress_warnings=True, 
                                    stepwise=True)
            # fmt: on
            self.order = auto_model.order
            self.seasonal_order = auto_model.seasonal_order
            self.trained_model = auto_model.fit(data)
        else:
            model = ARIMA(data, order=self.order, seasonal_order=self.seasonal_order)
            self.trained_model = model.fit(data)

    def evaluate(self, actual, forecasted):
        return mean_absolute_error(actual, forecasted)

    def predict(self, steps):
        if self.auto_arima_enabled:
            return self.trained_model.predict(n_periods=steps)
        else:
            return self.trained_model.forecast(steps=steps)
