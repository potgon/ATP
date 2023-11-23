import talib as ta
import pandas as pd
from typing import Callable

from utils.logger import make_log


def find_patterns(df: pd.DataFrame, patterns: list) -> pd.DataFrame:
    data = df.copy()
    for pattern in patterns:
        data[pattern] = pattern_factory(pattern)(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        make_log(
            "CDL",
            20,
            "workflow.log",
            f"Found {len(data[pattern])} {pattern} data points",
        )

    return data


def pattern_factory(pattern: str):
    if pattern == "Engulfing":
        return ta.CDLENGULFING
    elif pattern == "Doji":
        return ta.CDLDOJI
    elif pattern == "Hammer":
        return ta.CDLHAMMER
    elif pattern == "Inverted Hammer":
        return ta.CDLINVERTEDHAMMER
    elif pattern == "Shooting Star":
        return ta.SHOOTINGSTAR
    elif pattern == "Hanging Man":
        return ta.CDLHANGINGMAN
    elif pattern == "Morning Star":
        return ta.CDLMORNINGSTAR
    elif pattern == "Evening Star":
        return ta.CDLEVENINGSTAR
    elif pattern == "Harami":
        return ta.CDLHARAMI
    elif pattern == "Three Black Crows":
        return ta.CDL3BLACKCROWS
    elif pattern == "Three White Soldiers":
        return ta.CDL3WHITESOLDIERS
    elif pattern == "Dark Cloud Cover":
        return ta.CDLDARKCLOUDCOVER
    elif pattern == "Piercing":
        return ta.CDLPIERCING
    else:
        raise ValueError("Unknown Pattern")
