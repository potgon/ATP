import talib as ta
import pandas as pd

from data_processing.pattern_recog import find_patterns
from utils.config import MAX_CDL_CONTRIBUTION


class Tyr:
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def evaluate(self, data) -> bool:
        data = self.preprocess_data(self.fetcher.current_data.copy())
        return (
            self.evaluate_RSI(data) + self.evaluate_CDL(data) + self.evaluate_SNR(data)
        ) > 5

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        patterns = [
            "Engulfing",
            "Morning Star",
            "Three White Soldiers",
            "Doji",
            "Hammer",
            "Inverted Hammer",
            "Evening Star",
            "Three Black Crows",
            "Shooting Star",
            "Hanging Man",
        ]
        data = find_patterns(data, patterns)
        data["RSI"] = ta.RSI(data["Close"], timeperiod=14)

        return data

    def evaluate_RSI(self, data) -> int:
        return (
            3
            if data["RSI"].iloc[-1] <= 30
            else (-3 if data["RSI"].iloc[-1] >= 70 else 0)
        )

    def evaluate_CDL(self, data):
        alpha = 0
        patterns = {
            "Engulfing": 2,
            "Morning Star": 2,
            "Three White Soldiers": 2,
            "Doji": 1,
            "Hammer": 1,
            "Inverted Hammer": 1,
            "Evening Star": -2,
            "Three Black Crows": -2,
            "Shooting Star": -1,
            "Hanging Man": -1,
        }

        for i in range(-3, 0):
            for pattern, value in patterns.items():
                if data[pattern].iloc[i] == 100:
                    alpha += value
                elif data[pattern].iloc[-1] == -100:
                    alpha -= value

        alpha = max(min(alpha, MAX_CDL_CONTRIBUTION), -MAX_CDL_CONTRIBUTION)
        return alpha

    def evaluate_SNR(self):
        pass
