from utils.config import RSI_CONSTANT


def evaluate(data) -> bool:
    alpha = 0
    # alpha += evaluate_RSI(data["RSI"])
    rsi_eval = evaluate_RSI(data["RSI"])
    pass


def evaluate_RSI(RSI) -> bool:
    return RSI / RSI_CONSTANT


def evaluate_VOL():
    pass


def evaluate_CDL():
    pass


def evaluate_SUP():
    pass
