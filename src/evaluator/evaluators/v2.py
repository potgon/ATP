import pandas as pd

from data_processing.fetcher import Fetcher
from data_processing.indicators import Indicators
from utils.config import RSI_CONSTANT

fetcher: Fetcher = Fetcher("EURUSD=X")


def evaluate(data) -> bool:
    alpha: int = 0
    # rsi_eval = evaluate_RSI(data["RSI"])
    pass


def sentiment_eval() -> float:
    pass


# def evaluate_RSI(RSI) -> bool:
#     return RSI / RSI_CONSTANT


def evaluate_VOL():
    pass


def evaluate_CDL():
    pass


def evaluate_SUP():
    pass
