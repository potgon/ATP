from datetime import datetime
from decimal import Decimal

import pandas as pd
from aws.db import execute_sql
from utils.logger import make_log


def insert_transaction(data: pd.Series, alpha: int) -> None:
    params = (datetime.now(), Decimal(data["Open"]), alpha)
    make_log(
        "TRACKER",
        20,
        "tracker.log",
        execute_sql(
            """
           INSERT INTO test_transactions (date_open, open_price, alpha) VALUES (%s, %s, %s)      
        """,
            params,
        ),
    )


def alter_transaction(data: pd.Series) -> None:
    params = (
        datetime.now(),
        Decimal(data["Close"]),
        Decimal(data["Close"]),
    )
    make_log(
        "TRACKER",
        20,
        "tracker.log",
        execute_sql(
            """
        UPDATE test_transactions
        SET date_close = %s, close_price = %s, net_profit = %s - (SELECT open_price FROM test_transactions WHERE id = (SELECT MAX(id) FROM test_transactions))
        WHERE id = (SELECT MAX(id) FROM test_transactions)
        """,
            params,
        ),
    )
