import yfinance as yf
import talib as ta
import threading
import pandas as pd
import numpy as np

from utils.logger import make_log
from utils.config import (
    SNR_CLOSENESS_FACTOR,
    SNR_MIN_BOUNCES,
    SNR_PROPORTIONALITY_RATIO,
    SNR_DEVIATION_FACTOR,
)
from evaluator.evaluator_factory import get_evaluator
from app.snr import pivotid, pointpos


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

    # data["RSI"] = ta.RSI(data["Close"], timeperiod=14)
    # data["ATR"] = ta.ATR(data["High"], data["Low"], data["Close"], timeperiod=90)

    data["Pivot"] = data.apply(lambda x: pivotid(data, x.name, 10, 10), axis=1)
    data["Pointpos"] = data.apply(lambda row: pointpos(row), axis=1)
    # TODO: Move this into a snr function. Mix highs and lows, calculate c_factor and separate again
    high_counts = data[data["Pivot"] == 2]["High"].value_counts()
    low_counts = data[data["Pivot"] == 1]["Low"].value_counts()

    significant_highs = high_counts[high_counts >= SNR_MIN_BOUNCES]
    significant_lows = low_counts[low_counts >= SNR_MIN_BOUNCES]

    filtered_highs, filtered_lows = [], []

    avg_price = data["Close"].mean()
    make_log("FETCHER", 20, "workflow.log", f"Data Average Price: {avg_price}")
    c_factor = avg_price * SNR_PROPORTIONALITY_RATIO
    make_log("FETCHER", 20, "workflow.log", f"C_Factor: {c_factor}")
    for level in significant_highs.index:
        if not any(
            abs(level - other_level) < SNR_CLOSENESS_FACTOR
            for other_level in filtered_highs
        ):
            filtered_highs.append(level)

    for level in significant_lows.index:
        if not any(
            abs(level - other_level) < SNR_CLOSENESS_FACTOR
            for other_level in filtered_lows
        ):
            filtered_lows.append(level)

    data["Resistance"] = data["High"].apply(
        lambda x: x if x in filtered_highs else np.nan
    )
    data["Support"] = data["Low"].apply(lambda x: x if x in filtered_lows else np.nan)

    return data


def remove_nan_rows(data: pd.DataFrame) -> pd.DataFrame:
    updated_data = data.copy()
    # updated_data = updated_data[updated_data["Volume"] != 0]
    updated_data.reset_index(inplace=True)

    return updated_data
