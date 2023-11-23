import yfinance as yf
import talib as ta
import threading
import pandas as pd

from utils.logger import make_log
from evaluator.evaluator_factory import get_evaluator


class Fetcher:
    def __init__(self, ticker="AAPL") -> None:
        self.ticker = ticker
        self.current_data = self._initialise_data()
        self.data_lock = threading.Lock()

    def _initialise_data(self, period="730d", interval="1h") -> pd.DataFrame:
        return fetch_indicator_data(self.ticker, period, interval)

    def fetch(self) -> pd.Series:
        make_log("FETCHER", 20, "workflow.log", "Fetching new data...")
        temp_data = fetch_indicator_data(self.ticker)
        if temp_data.index[0] not in self.current_data.index:
            with self.data_lock:
                self.current_data = pd.concat([self.current_data, temp_data], axis=0)
            make_log("FETCHER", 20, "workflow.log", "Appended new data")
        make_log(
            "FETCHER",
            20,
            "workflow.log",
            f"Fetched {len(self.current_data)} data points for {self.ticker}.",
        )
        return temp_data


def fetch_indicator_data(
    ticker="EURUSD=X", period="730d", interval="1h"
) -> pd.DataFrame:
    data = yf.download(ticker, period=period, interval=interval)
    data = remove_nan_rows(data)
    return data


def remove_nan_rows(data: pd.DataFrame) -> pd.DataFrame:
    updated_data = data.copy()
    # updated_data = updated_data[updated_data["Volume"] != 0]
    updated_data.reset_index(inplace=True)

    return updated_data
