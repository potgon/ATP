import time


class Position:
    def __init__(self, close: float, atr: float, logger) -> None:
        self.sl = calculate_atr_sl(close, atr)
        self.tp = calculate_ratio_tp(close, self._sl)
        self.timestamp = time.now()
        self.logger = logger

    # API functionality to close position
    def close(self):
        self.logger.info("Position closed")

    # API functionality to open position
    def open(self):
        self.logger.info("Position opened")


def calculate_atr_sl(close: float, atr: float) -> float:
    return close - (atr * 2)


def calculate_ratio_tp(close: float, sl: float) -> float:
    return (abs(close - sl) * 1.5) + close


def close_position(data, sl: float, tp: float) -> bool:
    data = data.iloc[-1]
    return data["Low"] <= sl or data["High"] >= tp
