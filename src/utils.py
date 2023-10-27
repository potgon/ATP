import datetime 
import yfinance as yf
import asyncio
import concurrent.futures
import talib as ta
import pandas as pd
import numpy as np
import mplfinance as mpf
import logger as lg

current_data = pd.DataFrame()
logger = lg.setup_logger("utils")

async def fetch_indicator_data():
    
    data = yf.download("AAPL", period="1d", interval="1m")

    data['Upper'], data['Middle'], data['Lower'] = ta.BBANDS(data['Close'], timeperiod=12, nbdevup=2, nbdevdn=2, matype=0)
    data['EMA9'] = ta.EMA(data['Close'], timeperiod=9)
    data['EMA21'] = ta.EMA(data['Close'], timeperiod=21)
    return data


async def periodic_fetch():
    global current_data
    while True:
        current_data = await fetch_indicator_data()
        logger.info(f"Fetched {len(current_data)} data points for AAPL.")
        await asyncio.sleep(60*5)


def buy_signal(data):
    return (data['Close'] <= data['Lower']) & (data['EMA9'] > data['EMA21'])
