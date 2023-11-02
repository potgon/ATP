import yfinance as yf
import talib as ta
import time
import threading
import pandas as pd

import utils.logger as lg
import utils.data as dt
from evaluator.evaluator_factory import get_evaluator


class Fetcher:
    def __init__(self, ticker="AAPL") -> None:
        self.ticker = ticker
        self.current_data = self._initialise_data()
        self.data_lock = threading.Lock()
        self.logger = lg.setup_custom_logger("fetcher")

    def _initialise_data(self, period="1d", interval="1m") -> pd.DataFrame:
        return _fetch_indicator_data(self.ticker, period, interval)

    def periodic_fetch(self):
        while True:
            temp_data = _fetch_indicator_data(self.ticker)
            if temp_data.index[0] not in self.current_data.index:
                with self.data_lock:
                    self.current_data = pd.concat(
                        [self.current_data, temp_data], axis=0
                    )
                    print(self.current_data.tail())
            dt.calculate_all_sl(self.current_data)
            dt.calculate_all_tp(self.current_data)
            self.logger.info(
                f"Fetched {len(self.current_data)} data points for {self.ticker}."
            )
            time.sleep(60)


def _fetch_indicator_data(ticker="AAPL", period="1d", interval="1m"):
    data = yf.download(ticker, period=period, interval=interval)

    data["Upper"], data["Middle"], data["Lower"] = ta.BBANDS(
        data["Close"], timeperiod=12, nbdevup=2, nbdevdn=2, matype=0
    )
    data["EMA9"] = ta.EMA(data["Close"], timeperiod=9)
    data["EMA21"] = ta.EMA(data["Close"], timeperiod=21)
    data["ATR"] = ta.ATR(data["High"], data["Low"], data["Close"], timeperiod=14)
    data["Buy Signal"] = get_evaluator()(data)
    data["Stop Loss"] = pd.Series()
    data["Take Profit"] = pd.Series()
    # data = dt.calculate_slope(data, data["EMA9"])
    # data['Swing_Low'] = data['Low'].rolling(window=3).apply(dt.is_swing_low)
    return data
