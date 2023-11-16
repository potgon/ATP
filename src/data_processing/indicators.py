import pandas as pd
import talib as ta

from data_processing.fetcher import Fetcher


class Indicators:
    def __init__(self, ticker):
        self.fetcher = Fetcher(ticker)

    def get_RSI(self):
        with self.fetcher.data_lock:
            data = self.fetcher.current_data.copy()
            data["RSI"] = ta.RSI(data["Close"], timeperiod=14)
        return data

    def get_ATR(self):
        with self.fetcher.data_lock:
            data = self.fetcher.current_data.copy()
            data["ATR"] = ta.ATR(
                data["High"], data["Low"], data["Close"], timeperiod=14
            )
        return data

    def get_EMA(self, period: int):
        with self.fetcher.data_lock:
            data = self.fetcher.current_data.copy()
            data["EMA"] = ta.EMA(data["Close"], timeperiod=period)
        return data


def remove_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    updated_data = df.copy()
    updated_data = updated_data[updated_data["Volume"] != 0]
    updated_data.reset_index(inplace=True)

    return updated_data
