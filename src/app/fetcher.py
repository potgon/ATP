import yfinance as yf
import talib as ta
import time
import threading
import pandas as pd

import utils.logger as lg

class Fetcher:
    def __init__(self) -> None:
        self.current_data = self._initialise_data()
        self.data_lock = threading.Lock()
        self.logger = lg.setup_logger("fetcher")

    def _initialise_data(self, period="5d", interval="1m") -> pd.DataFrame:
        return _fetch_indicator_data(period, interval)

    def periodic_fetch(self):
        while True:
            temp_data = _fetch_indicator_data(period="1m")
            if temp_data.index[0] not in self.current_data.index:
                with self.data_lock:
                    self.current_data = pd.concat(
                        [self.current_data, temp_data], axis=0
                    )
                    print(self.current_data.tail())
            self.logger.info(f"Fetched {len(self.current_data)} data points for AAPL.")
            self.logger.info(f"Utils data ID: {id(self.current_data)}")
            time.sleep(60)


def _fetch_indicator_data(period="5d", interval="1m"):
    data = yf.download("AAPL", period=period, interval=interval)

    data["Upper"], data["Middle"], data["Lower"] = ta.BBANDS(
        data["Close"], timeperiod=12, nbdevup=2, nbdevdn=2, matype=0
    )
    data["EMA9"] = ta.EMA(data["Close"], timeperiod=9)
    data["EMA21"] = ta.EMA(data["Close"], timeperiod=21)
    data = calculate_slope(data, data['EMA9'])
    return data

def calculate_slope(data: pd.DataFrame, ema_series: pd.Series) -> pd.DataFrame:
    data['EMA'] = ema_series
    data['Slope'] = data['EMA'].diff()
    return data