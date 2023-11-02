# def evaluate(data) -> bool:
#    return (data["Close"] <= data["Lower"]) & (data["EMA9"] > data["EMA21"])


def evaluate(data) -> bool:
    return (bbands_relative_value(data) <= 0.5) & (data["EMA9"] > data["EMA21"])


def bbands_relative_value(data):
    data["Relative_Position"] = (data["Close"] - data["Lower"]) / (
        data["Middle"] - data["Lower"]
    )
    return data["Relative_Position"]
