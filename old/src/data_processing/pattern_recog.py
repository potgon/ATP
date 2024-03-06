from typing import Callable

import pandas as pd
import talib as ta


def find_patterns(df: pd.DataFrame, pattern_list: list) -> pd.DataFrame:
    data = df.copy()
    for pattern in pattern_list:
        data[pattern] = pattern_factory(pattern)(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
    return data


def pattern_factory(pattern: str) -> Callable:
    if pattern == "Engulfing":
        return ta.CDLENGULFING
    elif pattern == "Doji":
        return ta.CDLDOJI
    elif pattern == "Hammer":
        return ta.CDLHAMMER
    elif pattern == "Inverted Hammer":
        return ta.CDLINVERTEDHAMMER
    elif pattern == "Shooting Star":
        return ta.CDLSHOOTINGSTAR
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
