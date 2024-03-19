from collections import deque
import tensorflow as tf

from .model_base import ModelTrainer
from .window_pipeline import data_processing


class Trainer(ModelTrainer):
    def __init__(self):
        self.val_performance, self.performance = {}
        self.queue = deque()
        self.prio_queue = deque()
        self.current_model_instance = None
        self.current_trained_model = None

    def enqueue_model(self, model, user):
        # Check if user is prio
        # if user.prio:
        self.prio_queue.append(model)
        # else:
        self.queue.append(model)

    def _get_next_model_instance(self):
        return self.prio_queue.pop() if self.prio_queue else self.queue.pop()

    def _compile_and_fit(model, window, epochs=20, patience=2):
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=patience, mode="min"
        )
        model.compile(
            loss=tf.losses.MeanSquaredError(),
            optimizer=tf.optimizers.Adam(),
            metrics=[tf.metrics.MeanAbsoluteError()],
        )
        history = model.fit(
            window.train,
            epochs=epochs,
            validation_data=window.val,
            callbacks=[early_stopping],
        )

        return history

    def train(self):
        self.current_model_instance = self._get_next_model_instance()
        self.current_trained_model = self._compile_and_fit(
            self.current_model_instance.model, self.current_model_instance.window
        )

    def evaluate(self):
        pass

    def predcit(self):
        pass
