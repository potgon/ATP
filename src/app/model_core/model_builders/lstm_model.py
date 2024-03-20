import tensorflow as tf

from model_core.window_pipeline import data_processing


class LSTMModel:
    def __init__(self, window, units=50):
        self.window = data_processing("data\datasets\SP500_data.csv")
        self.units = units
        self.model = self.build_model()

    def build_model(self):
        self.model = tf.keras.Sequential(
            [
                tf.keras.layers.LSTM(self.units, return_sequences=False),
                tf.keras.layers.Dense(1),
            ]
        )

        self.model.compile(optimizer="adam", loss="mse")
