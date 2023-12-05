import talib as ta
import pandas as pd

from aws.db import execute_sql
from data_processing.pattern_recog import find_patterns
from utils.config import MAX_CDL_CONTRIBUTION
from utils.logger import make_log

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


class Tyr:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.alpha = 0

    def evaluate(self) -> bool:
        data = self._preprocess_data(self.fetcher.current_data.copy())
        alpha = (
            self._evaluate_RSI(data)
            + self._evaluate_CDL(data)
            + self._evaluate_SNR(data)
        )
        self.alpha = alpha
        make_log("TYR", 20, "workflow.log", f"alpha: {alpha}")
        return alpha > 5

    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = find_patterns(data, list(patterns.keys()))
        data["RSI"] = ta.RSI(data["Close"], timeperiod=14)

        return data

    def _evaluate_RSI(self, data: pd.DataFrame) -> int:
        alpha = (
            3
            if data["RSI"].iloc[-1] <= 30
            else (-3 if data["RSI"].iloc[-1] >= 70 else 0)
        )
        make_log("TYR", 20, "workflow.log", f"RSI contribution: {alpha}")
        return alpha

    def _evaluate_CDL(self, data: pd.DataFrame):
        alpha = 0

        for i in range(-3, 0):
            for pattern, value in patterns.items():
                if data[pattern].iloc[i] == 100:
                    alpha += value
                elif data[pattern].iloc[-1] == -100:
                    alpha -= value

        alpha = max(min(alpha, MAX_CDL_CONTRIBUTION), -MAX_CDL_CONTRIBUTION)
        make_log("TYR", 20, "workflow.log", f"CDL contribution: {alpha}")
        return alpha

    def evaluate_SNR(self, data: pd.DataFrame):
        reversal_dict = get_snr_prices(self.fetcher.ticker)

        for max, min in reversal_dict.items():
            if min <= data["Close"].iloc[-1] <= max:
                make_log("TYR", 20, "workflow.log", f"RSI contribution: 3")
                return 3

        return 0


def get_snr_prices(ticker: str) -> dict:
    reversal_range = {}
    sql_result = execute_sql(
        "SELECT price_range_max FROM reversal_zones WHERE asset_id = (SELECT id FROM assets WHERE name = %s)",
        (ticker,),
    )
    reversals_max = [float(i) for i in sql_result]
    sql_result = execute_sql(
        "SELECT price_range_min FROM reversal_zones WHERE asset_id = (SELECT id FROM assets WHERE name = %s)",
        (ticker,),
    )
    reversals_min = [float(i) for i in sql_result]
    for i in range(len(reversals_max)):
        reversal_range[reversals_max[i]] = reversals_min[i]

    make_log(
        "TYR",
        20,
        "workflow.log",
        f"Fetched: {len(reversal_range)} reversal zones for {ticker}",
    )

    return reversal_range
