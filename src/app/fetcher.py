import yfinance as yf
import talib as ta
import threading
import pandas as pd

import utils.logger as lg
from evaluator.evaluator_factory import get_evaluator


class Fetcher:
    def __init__(self, ticker="AAPL") -> None:
        self.ticker = ticker
        self.current_data = self._initialise_data()
        self.data_lock = threading.Lock()
        self.logger = lg.setup_custom_logger("fetcher")

    def _initialise_data(self, period="1d", interval="1m") -> pd.DataFrame:
        return _fetch_indicator_data(self.ticker, period, interval)

    def fetch(self) -> pd.Series:
        temp_data = _fetch_indicator_data(self.ticker)
        if temp_data.index[0] not in self.current_data.index:
            with self.data_lock:
                self.current_data = pd.concat([self.current_data, temp_data], axis=0)
        self.logger.info(
            f"Fetched {len(self.current_data)} data points for {self.ticker}."
        )
        return temp_data


def _fetch_indicator_data(ticker="AAPL", period="1d", interval="1m"):
    data = yf.download(ticker, period=period, interval=interval)

    data["Upper"], data["Middle"], data["Lower"] = ta.BBANDS(
        data["Close"], timeperiod=12, nbdevup=2, nbdevdn=2, matype=0
    )
    data["EMA9"] = ta.EMA(data["Close"], timeperiod=9)
    data["EMA21"] = ta.EMA(data["Close"], timeperiod=21)
    data["ATR"] = ta.ATR(data["High"], data["Low"], data["Close"], timeperiod=14)
    return data
