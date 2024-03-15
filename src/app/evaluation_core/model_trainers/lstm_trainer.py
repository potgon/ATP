import tensorflow as tf

from src.app.evaluation_core.model_core.model_base import ModelTrainer

class LSTMTrainer(ModelTrainer):
    
    def __init__(self, window, units):
        self.window = window
        self.units = units
        self.model = None

    def build_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.LSTM(self.units, return_sequences=False),
            tf.keras.layers.Dense(1)
        ])
        
        self.model.compile(optimizer="adam", loss="mse")
        
    def train(self):
        self.build_model()
        return compile_and_fit(self.model, self.window)
    
    def evaluate(self):
        return self.model.evaluate(self.window.test)
    
    def predict(self):
        return self.model.predict(self.window.test)
    
    
    
# I should put this function somewhere else
def compile_and_fit(model, window, epochs=20, patience=2):
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                      patience=patience,
                                                      mode="min")
    model.compile(loss=tf.losses.MeanSquaredError(),
                  optimizer=tf.optimizers.Adam(),
                  metrics=[tf.metrics.MeanAbsoluteError()])
    history = model.fit(window.train, epochs=epochs,
                        validation_data=window.val,
                        callbacks=[early_stopping])
    return history
    