from collections import deque
import tensorflow as tf

from .models import TrainedModel, ModelType
from .model_base import ModelTrainer


class Trainer(ModelTrainer):
    def __init__(self):
        self.val_performance, self.performance = {}
        self.queue = deque()
        self.prio_queue = deque()
        self.priority_counter = 0
        self.current_model_instance = None
        self.current_trained_model = None

    def enqueue_model(self, user, asset, model):
        if user.prio:
            self.prio_queue.append((user, asset, model))
        else:
            self.queue.append((user, asset, model))

    def _get_next_tuple(self):
        if self.prio_queue and self.priority_counter < 5:
            self.priority_counter += 1
            return self.prio_queue.pop()
        else:
            self.priority_counter = 0
            return self.queue.pop()

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
        self.val_performance = self.current_trained_model.evaluate(
            self.current_model_instance.window.val
        )
        self.performance = self.current_trained_model.evaluate(
            self.current_model_instance.window.test, verbose=0
        )

    def predict(self):
        pass

    def save_model(self):
        self._save_new_model()

    def _save_new_model(self):
        model_str = self.current_model_instance.__str__()
        if not ModelType.objects.filter(name=model_str["model_name"]).exists():
            ModelType(
                name=model_str["model_name"],
                description=model_str["description"],
                default_hyperparameters=model_str["default_hyperparameters"],
                default_model_architecture=model_str["default_model_architecture"],
            ).save()
