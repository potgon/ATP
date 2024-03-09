from pmdarima import auto_arima
from sklearn.model_selection import train_test_split

from app.trading_data.fetcher import Fetcher


def data_init():
    fetcher = Fetcher("NG=F", start="2019-01-01", end="2022-01-01")
    return fetcher.current_data["Close"]


def parameter_tuning(data):
    # fmt: off
    optimal_model = auto_arima(data, start_p=0, start_q=0, 
                            max_p=5, max_q=5, m=12, 
                            start_P=0, seasonal=True, 
                            d=1, D=1, trace=True, 
                            error_action="ignore",
                            suppress_warnings=True, 
                            stepwise=True)
    return optimal_model
    # fmt: on
