import yfinance as yf
import talib as ta
import threading
import pandas as pd
import numpy as np

from utils.logger import make_log
from utils.config import CLUSTER_MIN_POINTS, CLUSTER_THRESHOLD
from evaluator.evaluator_factory import get_evaluator


class Fetcher:
    def __init__(self, ticker="AAPL") -> None:
        self.ticker = ticker
        self.current_data = self._initialise_data()
        self.current_snr = self._initialise_clusters()
        self.data_lock = threading.Lock()

    def _initialise_data(self, period="1d", interval="1m") -> pd.DataFrame:
        return fetch_indicator_data(self.ticker, period, interval)

    def _initialise_clusters(self) -> pd.DataFrame:
        return fetch_clusters(self.current_data)

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

    def update_snr(self) -> pd.Series:
        make_log(
            "FETCHER", 20, "workflow.log", "Checking for support and resistance zones"
        )
        temp_clusters = fetch_clusters(self.current_data)
        if temp_clusters.index[0] not in self.current_snr.index:
            with self.data_lock:
                self.current_snr = pd.concat([self.current_snr, temp_clusters], axis=0)
            make_log("FETCHER", 20, "workflow.log", "Appended new clusters")
        make_log(
            "FETCHER",
            20,
            "workflow.log",
            f"Fetched {len(self.current_snr)} clusters for {self.ticker}",
        )


def fetch_indicator_data(
    ticker="GBPUSD=X", period="30d", interval="1h"
) -> pd.DataFrame:
    data = yf.download(ticker, period=period, interval=interval)

    data["RSI"] = ta.RSI(data["Close"], timeperiod=14)
    data["ATR"] = ta.ATR(data["High"], data["Low"], data["Close"], timeperiod=14)

    ema = ta.EMA(data["Close"], timeperiod=14)
    data["1st Derivative"] = ema.diff()
    data["2nd Derivative"] = data["1st Derivative"].diff()
    data["Sign Change"] = np.sign(data["2nd Derivative"]).diff()
    data["Cluster"] = (data["Close"].diff().abs() > CLUSTER_THRESHOLD).cumsum()
    return data


def fetch_clusters(data: pd.DataFrame) -> pd.DataFrame:
    valid_cluster_bool = data.groupby("Cluster")["Close"].transform(
        lambda x: len(x) >= CLUSTER_MIN_POINTS
    )
    valid_cluster_data = data[valid_cluster_bool]
    return valid_cluster_data.groupby("Cluster")["Close"].agg(["min", "max"])
