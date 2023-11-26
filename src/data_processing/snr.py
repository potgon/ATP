import numpy as np
import pandas as pd

from app.dash_app import retrieve_fetcher
from utils.config import (
    SNR_MIN_BOUNCES,
    SNR_PROPORTIONALITY_RATIO,
    SNR_PERCENTAGE_RANGE,
)
from utils.logger import log_full_dataframe, make_log

fetcher = retrieve_fetcher()


def get_pivots():
    with fetcher.data_lock:
        data = fetcher.current_data
    data["Pivot"] = data.apply(lambda x: pivotid(data, x.name, 10, 10), axis=1)
    data["Pointpos"] = data.apply(lambda row: pointpos(row), axis=1)

    high_counts = data[data["Pivot"] == 2]["High"].value_counts()
    low_counts = data[data["Pivot"] == 1]["Low"].value_counts()

    significant_highs = high_counts[high_counts >= SNR_MIN_BOUNCES]
    significant_lows = low_counts[low_counts >= SNR_MIN_BOUNCES]

    filtered_highs, filtered_lows = [], []

    avg_price = data["Close"].mean()
    make_log("SNR", 20, "workflow.log", f"Data Average Price: {avg_price}")
    c_factor = avg_price * SNR_PROPORTIONALITY_RATIO
    make_log("SNR", 20, "workflow.log", f"C_Factor: {c_factor}")
    for level in significant_highs.index:
        if not any(
            abs(level - other_level) < c_factor for other_level in filtered_highs
        ):
            filtered_highs.append(level)

    for level in significant_lows.index:
        if not any(
            abs(level - other_level) < c_factor for other_level in filtered_lows
        ):
            filtered_lows.append(level)

    data["Resistance"] = data["High"].apply(
        lambda x: x if x in filtered_highs else np.nan
    )
    data["Support"] = data["Low"].apply(lambda x: x if x in filtered_lows else np.nan)

    return data


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


def calculate_reversal_zones(avg_price: float) -> pd.DataFrame:
    data = get_pivots()
    range_value = get_range_value(avg_price)
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
    reversal_zones = pd.DataFrame(reversal_zones_data)
    filtered_zones = remove_close_zones(reversal_zones, avg_price)
    make_log(
        "SNR",
        20,
        "workflow.log",
        f"Unfiltered zones: {reversal_zones.shape[0]} | Filtered zones: {filtered_zones.shape[0]}",
    )
    return filtered_zones


def get_range_value(avg_price: float) -> float:
    make_log("SNR", 20, "workflow.log", f"Average Price: {avg_price}")
    return avg_price * SNR_PERCENTAGE_RANGE


def remove_close_zones(df: pd.DataFrame, avg_price: float):
    data = df.copy()
    combined_c_factor = avg_price * SNR_PROPORTIONALITY_RATIO
    combined_prices = (
        pd.concat([data["Min"], data["Max"]]).sort_values().reset_index(drop=True)
    )
    price_diffs = combined_prices.diff().abs()
    valid_prices = price_diffs > combined_c_factor
    make_log("SNR", 20, "workflow.log", f"Current range threshold: {combined_c_factor}")
    filtered_prices = combined_prices[valid_prices]
    valid_df = data[
        data["Min"].isin(filtered_prices) | data["Max"].isin(filtered_prices)
    ]
    return valid_df
