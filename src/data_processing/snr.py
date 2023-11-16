import numpy as np
import pandas as pd

from utils.config import SNR_MIN_BOUNCES, SNR_CLOSENESS_FACTOR


def get_snr(df: pd.DataFrame):
    data = df.copy()

    data["Pivot"] = data.apply(lambda x: pivotid(data, x.name, 10, 10), axis=1)
    data["Pointpos"] = data.apply(lambda row: pointpos(row), axis=1)

    high_counts = data[data["Pivot"] == 2]["High"].value_counts()
    low_counts = data[data["Pivot"] == 1]["Low"].value_counts()

    significant_highs = high_counts[high_counts >= SNR_MIN_BOUNCES]
    significant_lows = low_counts[low_counts >= SNR_MIN_BOUNCES]

    filtered_highs, filtered_lows = [], []

    for level in significant_highs.index:
        if not any(
            abs(level - other_level) < SNR_CLOSENESS_FACTOR
            for other_level in filtered_highs
        ):
            filtered_highs.append(level)

    for level in significant_lows.index:
        if not any(
            abs(level - other_level) < SNR_CLOSENESS_FACTOR
            for other_level in filtered_lows
        ):
            filtered_lows.append(level)

    data["Resistance"] = data["High"].apply(
        lambda x: x if x in filtered_highs else np.nan
    )
    data["Support"] = data["Low"].apply(lambda x: x if x in filtered_lows else np.nan)

    return data  # Logic to store values in the RDS database


def pivotid(df1, l, n1, n2):
    if l - n1 < 0 or l + n2 >= len(df1):
        return 0

    pividlow = 1
    pividhigh = 1
    for i in range(l - n1, l + n2 + 1):
        if df1.Low[l] > df1.Low[i]:
            pividlow = 0
        if df1.High[l] < df1.High[i]:
            pividhigh = 0
    if pividlow and pividhigh:
        return 3
    elif pividlow:
        return 1
    elif pividhigh:
        return 2
    else:
        return 0


def pointpos(x):
    if x["Pivot"] == 1:
        return x["Low"] - 1e-3
    elif x["Pivot"] == 2:
        return x["High"] + 1e-3
    else:
        return np.nan
