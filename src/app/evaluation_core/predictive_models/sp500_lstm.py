import pandas as pd
import numpy as np

from app.evaluation_core.model_core.window_pipeline import data_init, data_processing
from app.evaluation_core.model_trainers.lstm_trainer import LSTMTrainer

class SP500LSTMModel:
    def __init__(self, units=50):
        self._LSTMTrainer = LSTMTrainer(window=data_processing(self.feature_engineering()), units=units) # Refactor, ping-pong is no bueno
        self.trained_model = None
        
    def train(self):
        self.trained_model = self.LSTMTrainer.train()

    def evaluate(self):
        # Look what does the inner-most evaluate do (print, plot...)
        # self.LSTMTrainer.evaluate()
        pass

    def predict(self):
        pass
