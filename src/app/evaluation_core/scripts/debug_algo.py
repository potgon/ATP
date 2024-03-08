# from app.evaluation_core.factories import get_evaluator
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# from app.trading_data.fetcher import Fetcher

# def init_algo():
# evaluator = get_evaluator(Fetcher("NG=F"), "FRIGG")


def draw_fig():
    data = yf.download("NG=F", start="2019-01-01", end="2022-01-01")
    plt.figure(figsize=(10, 5))
    plt.plot(data["Close"])
    plt.title("NATGAS Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return image_base64
