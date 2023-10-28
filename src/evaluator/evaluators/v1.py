def evaluate(data) -> bool:
    return (data["Close"] <= data["Lower"]) & (data["EMA9"] > data["EMA21"])
