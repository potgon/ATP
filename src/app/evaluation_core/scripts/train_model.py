import numpy as np

from app.evaluation_core.predictive_models.natgas_arima import NatgasARIMAModel
from app.utils.logger import make_log


def train_and_evaluate():
    model = NatgasARIMAModel(auto_arima_enabled=True)
    data = model.data_init(start_date="2015-01-01", end_date="2021-12-31")

    split_idx = int(len(data) * 0.8)
    train_data, test_data = data[:split_idx], data[split_idx:]

    train_mean = train_data.mean()
    train_std = train_data.std()

    train_data = (train_data - train_mean) / train_std
    test_data = (test_data - train_mean) / train_std

    model.train(train_data)

    predictions = model.predict(steps=len(test_data))

    actual = test_data.values
    error = np.mean(np.abs(predictions - actual) / actual)

    make_log(
        "NATGAS", 20, "algorithm.log", f"Model Evaluation (MAPE): {error * 100:.2f}%"
    )
    make_log(
        "NATGAS",
        20,
        "algorithm.log",
        f" \n Model summary: \n {model.trained_model.summary()}",
    )
    # model.save_model("natgas_arima_model.joblib")


if __name__ == "__main__":
    train_and_evaluate()
