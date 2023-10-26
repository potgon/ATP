import yfinance as yf
import talib

def get_aapl():
    
    ticker = "AAPL"

    data = yf.download(ticker, period="1d", interval="1m")

    print(data.head())
    
if __name__ == "__main__":
    get_aapl()