import talib as ta
import pandas as pd


class Tyr:
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def evaluate(self, data) -> bool:
        alpha: int = 0
        pass

    def preprocess_data(self) -> pd.DataFrame:
        data = self.fetcher.current_data.copy()
        data["RSI"] = ta.RSI(data["Close"], timeperiod=14)

        return data

    def evaluate_RSI(self, RSI) -> int:
        return 2 if RSI <= 30 else (-2 if RSI >= 70 else 0)

    def evaluate_CDL(self):
        pass

    def evaluate_SNR(self):
        pass
