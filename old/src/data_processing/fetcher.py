import threading

import pandas as pd
import talib as ta
import yfinance as yf
from requests.exceptions import ConnectionError, HTTPError, Timeout
from retrying import retry
from utils.config import FOREX_DATAFRAME_SIZE
from utils.logger import make_log


class Fetcher:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.current_data = self._initialise_data()
        self.data_lock = threading.Lock()

    def _initialise_data(self, period="30d", interval="1h") -> pd.DataFrame:
        return self._fetch_data(self.ticker, period, interval)

    def fetch(self) -> pd.Series:
        make_log("FETCHER", 20, "workflow.log", "Fetching new data...")
        temp_data = self._fetch_data(self.ticker)
        with self.data_lock:
            if temp_data.index[-1] not in self.current_data.index:
                self.current_data = pd.concat(
                    [self.current_data, temp_data], axis=0)
            make_log(
                "FETCHER",
                20,
                "workflow.log",
                f"Appended new data: {self.current_data['Close'].iloc[-1]}",
            )
            if len(self.current_data) > FOREX_DATAFRAME_SIZE:
                self.current_data = self.current_data.iloc[
                    -FOREX_DATAFRAME_SIZE:
                ].reset_index(drop=True)
            make_log("FETCHER", 20, "workflow.log", "Removed oldest data")
        make_log(
            "FETCHER",
            20,
            "workflow.log",
            f"Dataframe current size: {len(self.current_data)}",
        )
        return temp_data

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def _fetch_data(self, ticker, period="30d", interval="1h") -> pd.DataFrame:
        try:
            data = yf.download(ticker, period=period, interval=interval)
        except (HTTPError, ConnectionError, Timeout) as e:
            make_log(
                "FETCHER",
                40,
                "workflow.log",
                f"Network error while fetching {ticker} data with {period}/{interval}: {e} -> Retrying...",
            )
            raise
        except Exception as e:
            make_log(
                "FETCHER",
                40,
                "workflow.log",
                f"Unknown exception while fetching {ticker} data with {period}/{interval}: {e} -> Retrying...",
            )
            raise
        else:
            data["ATR"] = ta.ATR(
                data["High"], data["Low"], data["Close"], timeperiod=14
            )
            return self._remove_nan_rows(data)

    def _remove_nan_rows(self, data: pd.DataFrame) -> pd.DataFrame:
        updated_data = data.copy()
        if self.ticker[-2:] != "=X":
            updated_data = updated_data[updated_data["Volume"] != 0]
        updated_data.reset_index(inplace=True)

        return updated_data
