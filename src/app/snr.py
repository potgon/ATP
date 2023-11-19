import numpy as np
import pandas as pd

from utils.config import SNR_PERCENTAGE_RANGE


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


def calculate_reversal_zones(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    range_value = get_range_value(data)
    reversal_zones_data = []
    filtered_highs = data["Resistance"]
    filtered_lows = data["Support"]
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
    print(type(reversals))
    return reversals


def get_range_value(data: pd.DataFrame) -> float:
    avg_price = (data["High"].mean() + data["Low"].mean()) / 2
    print(avg_price * SNR_PERCENTAGE_RANGE)
    return avg_price * SNR_PERCENTAGE_RANGE
