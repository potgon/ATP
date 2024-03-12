import yfinance as yf
from sklearn.model_selection import train_test_split
from joblib import dump, load

from app.evaluation_core.model_trainers.arima_trainer import ARIMATrainer

# ARIMA model trained with NATGAS data


class NatgasARIMAModel:
    def __init__(self, order=None, seasonal_order=None, auto_arima_enabled=False):
        self.order = (
            None if auto_arima_enabled else order
        )  # Keep this logic only in arima_trainer
        self.seasonal_order = seasonal_order
        self.auto_arima_enabled = auto_arima_enabled
        self.arima_trainer = ARIMATrainer(
            order=self.order,
            seasonal_order=self.seasonal_order,
            auto_arima_enabled=self.auto_arima_enabled,
        )
        self.trained_model = None

    def data_init(self, ticker="NG=F", start_date="2019-01-01", end_date="2022-01-01"):
        data = yf.download(ticker, start=start_date, end=end_date)["Close"]
        return data

    def train(self, data):
        self.arima_trainer.train(data)
        if self.auto_arima_enabled:
            self.order = self.arima_trainer.order
            self.seasonal_order = self.arima_trainer.seasonal_order
        self.trained_model = self.arima_trainer.trained_model

    def save_model(self, filepath):
        dump(self.trained_model, filepath)

    def load_model(self, filepath):
        try:
            self.trained_model = load(filepath)
            self.arima_trainer.trained_model = self.trained_model
        except FileNotFoundError:
            print(
                f"Failed to load model from {filepath}"
            )  # Check logger module and implement custom logging

    def predict(self, steps=5):
        if self.trained_model:
            return self.arima_trainer.predict(steps)
        else:
            print(
                "Model not trained/loaded"
            )  # Check logger module and implement custom logging
            return None
