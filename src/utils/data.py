import pandas as pd


def calculate_slope(data: pd.DataFrame, ema_series: pd.Series) -> pd.DataFrame:
    """Calculates the slope given the DataFrame and the smoothed data of the EMA

    Args:
        data (pd.DataFrame): DataFrame containing the historical data.
        ema_series (pd.Series): Calculated EMA

    Returns:
        pd.DataFrame: DataFrame with slope appended
    """
    data["EMA"] = ema_series
    data["Slope"] = data["EMA"].diff()
    return data


# def is_swing_low(series):
#     return series[1] < series[0] and series[1] < series[2]


def find_swing_low(data: pd.DataFrame, window: int = 5) -> pd.Series:
    """Identify swing lows in a time series.

    Args:
        data (pd.DataFrame): DataFrame containing the historical data.
        window (int, optional): Number of data points to consider when identifying swing lows. Defaults to 5.

    Returns:
        pd.Series: Series of boolean values indicating if a data point is a swing low.
    """
    low = data["Low"]
    is_swing_low = (low.shift(1) > low) & (low < low.shift(-1))

    for i in range(2, window + 1):
        is_swing_low &= (low < low.shift(-i)) & (low < low.shift(i - 1))

    return is_swing_low


def calculate_fixed_sl(data: pd.DataFrame) -> float:
    return data["Close"].iloc[-1] * 0.98
