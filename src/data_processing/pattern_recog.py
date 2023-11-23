import talib as ta
import pandas as pd

from utils.logger import log_full_dataframe, make_log


def find_engulfing(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["Engulfing"] = ta.CDLENGULFING(
        data["Open"], data["High"], data["Low"], data["Close"]
    )

    return data
