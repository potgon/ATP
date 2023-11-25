import talib as ta
import pandas as pd

from data_processing.pattern_recog import find_patterns


class Tyr:
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def evaluate(self, data) -> bool:
        data = self.preprocess_data(self.fetcher.current_data.copy())
        return (
            self.evaluate_RSI(data) + self.evaluate_CDL(data) + self.evaluate_SNR(data)
        ) > 5

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        patterns = ["Doji", "Engulfing", "Hammer"]
        data = find_patterns(data, patterns)
        data["RSI"] = ta.RSI(data["Close"], timeperiod=14)

        return data

    def evaluate_RSI(self, data) -> int:
        return (
            2
            if data["RSI"].iloc[-1] <= 30
            else (-2 if data["RSI"].iloc[-1] >= 70 else 0)
        )

    def evaluate_CDL(self, data):
        pass

    def evaluate_SNR(self):
        pass
