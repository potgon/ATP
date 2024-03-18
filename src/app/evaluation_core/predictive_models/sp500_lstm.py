import pandas as pd
import numpy as np
import tensorflow as tf

from app.evaluation_core.model_core.window_pipeline import data_init, data_processing
from app.evaluation_core.model_trainers.lstm_trainer import LSTMTrainer

class LSTMModel:
    def __init__(self, units=50):
        self._LSTMTrainer = LSTMTrainer(window=data_processing(self.feature_engineering()), units=units) # Refactor, ping-pong is no bueno
        self.trained_model = None

    def feature_engineering(self) -> pd.DataFrame:
        df = data_init("data/datasets/SP500_data.csv", ["Dividends", "Stock Splits"])
        date_time = pd.to_datetime(df.pop("Date"), utc=True)
        df["day_of_week"] = date_time.dt.dayofweek
        df["month_of_year"] = date_time.dt.month

        df["day_sin"] = np.sin(df["day_of_week"] * (2 * np.pi / 7))
        df["day_cos"] = np.cos(df["day_of_week"] * (2 * np.pi / 7))
        df["month_sin"] = np.sin((df["month_of_year"] - 1) * (2 * np.pi / 12))
        df["month_cos"] = np.cos((df["month_of_year"] - 1) * (2 * np.pi / 12))

        return df
        
    def train(self):
        self.trained_model = self.LSTMTrainer.train()

    def evaluate(self):
        # Look what does the inner-most evaluate do (print, plot...)
        # self.LSTMTrainer.evaluate()
        pass

    def predict(self):
        pass
