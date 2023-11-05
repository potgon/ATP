from utils.config import RSI_CONSTANT


def evaluate(data) -> bool:
    alpha: int = 0
    rsi_eval = evaluate_RSI(data["RSI"])
    pass

def sentiment_eval() -> float:
    pass
    

def evaluate_RSI(RSI) -> bool:
    return RSI / RSI_CONSTANT


def evaluate_VOL():
    pass


def evaluate_CDL():
    pass


def evaluate_SUP():
    pass
