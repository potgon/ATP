import talib as ta
import pandas as pd


class Ymir:
    def __init__(self, fetcher):
        self.fetcher = fetcher

    def evaluate(self) -> bool:
        data = self.preprocess()
        return (self.bbands_relative_value(data) <= 0.33) & (
            data["EMA9"] > data["EMA21"]
        )

    def preprocess(self):
        data = self.fetcher.current_data
        data["RSI"] = ta.RSI(data["Close"], timeperiod=14)

        return data

    def bbands_relative_value(self, data):
        return (data["Close"] - data["Lower"]) / (data["Middle"] - data["Lower"])
