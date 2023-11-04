def evaluate(data) -> bool:
    return (bbands_relative_value(data) <= 0.33) & (data["EMA9"] > data["EMA21"])


def bbands_relative_value(data):
    return (data["Close"] - data["Lower"]) / (data["Middle"] - data["Lower"])
