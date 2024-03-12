import numpy as np

from app.evaluation_core.predictive_models.natgas_arima import NatgasARIMAModel


def train_and_evaluate():
    model = NatgasARIMAModel(auto_arima_enabled=True)
    data = model.data_init(start_date="2019-01-01", end_date="2021-12-31")

    split_idx = int(len(data) * 0.8)
    train_data, test_data = data[:split_idx], data[split_idx:]

    model.train(train_data)

    predictions = model.predict(steps=len(test_data))

    actual = test_data.values
    error = np.mean(np.abs(predictions - actual) / actual)

    print(f"Model Evaluation (MAPE): {error * 100:.2f}%")

    # model.save_model("natgas_arima_model.joblib")


if __name__ == "__main__":
    train_and_evaluate()
