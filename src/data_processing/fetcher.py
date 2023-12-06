import yfinance as yf
import threading
import pandas as pd
import talib as ta

from utils.logger import make_log
from utils.config import FOREX_DATAFRAME_SIZE


class Fetcher:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.current_data = self._initialise_data()
        self.data_lock = threading.Lock()

    def _initialise_data(self, period="30d", interval="1h") -> pd.DataFrame:
        return self._fetch_data(self.ticker, period, interval)

    def _fetch(self) -> pd.Series:
        make_log("FETCHER", 20, "workflow.log", "Fetching new data...")
        temp_data = self._fetch_data(self.ticker)
        with self.data_lock:
            if temp_data.index[0] not in self.current_data.index:
                self.current_data = pd.concat([self.current_data, temp_data], axis=0)
            make_log(
                "FETCHER",
                20,
                "workflow.log",
                f"Appended new data: \n {self.current_data.iloc[-1]}",
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

    def _fetch_data(self, ticker, period="30d", interval="1h") -> pd.DataFrame:
        data = yf.download(ticker, period=period, interval=interval)
        data["ATR"] = ta.ATR(data["High"], data["Low"], data["Close"], timeperiod=14)
        data = self._remove_nan_rows(data)
        return data

    def _remove_nan_rows(self, data: pd.DataFrame) -> pd.DataFrame:
        updated_data = data.copy()
        if self.ticker[-2:] != "=X":
            updated_data = updated_data[updated_data["Volume"] != 0]
        updated_data.reset_index(inplace=True)

        return updated_data
