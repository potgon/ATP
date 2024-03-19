import tensorflow as tf

from app.evaluation_core.model_core.model_base import ModelTrainer


class LSTMTrainer(ModelTrainer):

    def __init__(self, window, units):
        self.window = window
        self.units = units
        self.model = None

    def build_model(self):
        self.model = tf.keras.Sequential(
            [
                tf.keras.layers.LSTM(self.units, return_sequences=False),
                tf.keras.layers.Dense(1),
            ]
        )

        self.model.compile(optimizer="adam", loss="mse")

    def train(self):
        self.build_model()
        return compile_and_fit(self.model, self.window)

    def evaluate(self):
        return self.model.evaluate(self.window.test)

    def predict(self):
        return self.model.predict(self.window.test)
