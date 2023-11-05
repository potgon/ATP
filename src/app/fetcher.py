import yfinance as yf
import talib as ta
import threading
import pandas as pd
import numpy as np

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
        self.logger.info("Fetching new data...")
        temp_data = _fetch_indicator_data(self.ticker)
        if temp_data.index[0] not in self.current_data.index:
            with self.data_lock:
                self.current_data = pd.concat([self.current_data, temp_data], axis=0)
            self.logger.info("Appended new data")
        self.logger.info(
            f"Fetched {len(self.current_data)} data points for {self.ticker}."
        )
        return temp_data


def _fetch_indicator_data(ticker="GBPUSD=X", period="90d", interval="1d"):
    data = yf.download(ticker=ticker, period=period, interval=interval)
    
    data["RSI"] = ta.RSI(data["Close"], timeperiod=14)
    data["ATR"] = ta.ATR(data["High"], data["Low"], data["Close"], timeperiod=14)
    
    ema = ta.EMA(data["Close"], timeperiod=14)
    data["1st Derivative"] = ema.diff()
    data["2nd Derivative"] = data["1st Derivative"].diff()
    data["Sign Change"] = np.sign(data["2nd Derivative"]).diff()
    
    data["Cluster"] = (data["Close"].diff().abs() > 1).cumsum() #1 defines the threshold for price difference
    valid_clusters = data.groupby("Cluster")["Close"].filter(lambda x: len(x) >= 2) #2 defines the minimum points to consider a cluster as significant
    
    support_resistance = data[data["Cluster"].isin(valid_clusters["Cluster"])].groupby("Cluster")["Close"].agg(["min", "max"])
    return data