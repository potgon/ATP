import pandas as pd
import talib as ta

from data_processing.fetcher import Fetcher


class Indicators:
    def __init__(self, ticker):
        self.fetcher = Fetcher(ticker)

    def get_RSI(self):
        data = self.fetcher.current_data


def remove_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    updated_data = df.copy()
    updated_data = updated_data[updated_data["Volume"] != 0]
    updated_data.reset_index(inplace=True)

    return updated_data
