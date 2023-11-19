import numpy as np
import pandas as pd

from utils.config import SNR_PERCENTAGE_RANGE
from utils.logger import log_full_dataframe


def pivotid(data, idx, n1, n2):
    if idx - n1 < 0 or idx + n2 >= len(data):
        return 0

    pividlow = 1
    pividhigh = 1
    for i in range(idx - n1, idx + n2 + 1):
        if data.Low[idx] > data.Low[i]:
            pividlow = 0
        if data.High[idx] < data.High[i]:
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


def calculate_reversal_zones(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    range_value = get_range_value(data)
    reversal_zones_data = []
    filtered_highs = data["Resistance"].unique()
    filtered_lows = data["Support"].unique()
    for level in filtered_highs:
        price_range_max = level + range_value
        price_range_min = level - range_value
        reversal_zones_data.append(
            {
                "Type": "Resistance",
                "Price": level,
                "Max": price_range_max,
                "Min": price_range_min,
            }
        )
    for level in filtered_lows:
        price_range_max = level + range_value
        price_range_min = level - range_value
        reversal_zones_data.append(
            {
                "Type": "Support",
                "Price": level,
                "Max": price_range_max,
                "Min": price_range_min,
            }
        )
    reversals = pd.DataFrame(reversal_zones_data)
    log_full_dataframe("REVERSAL", 20, "reversals.log", reversals)
    return reversals


def get_range_value(data: pd.DataFrame) -> float:
    avg_price = (data["High"].mean() + data["Low"].mean()) / 2
    print(avg_price * SNR_PERCENTAGE_RANGE)
    return avg_price * SNR_PERCENTAGE_RANGE
