from datetime import datetime
from decimal import Decimal
import pandas as pd

from aws.db import execute_sql


def insert_transaction(data: pd.Series, alpha: int) -> None:
    params = (datetime.now(), Decimal(data["Open"]), alpha)
    execute_sql(
        """
           INSERT INTO test_transactions (date_open, open_price, alpha) VALUES (%s, %s, %s)      
        """,
        params,
    )


def alter_transaction(data: pd.Series) -> None:
    max_id_subquery = "(SELECT MAX(id) FROM test_transactions)"
    params = (
        datetime.now(),
        Decimal(data["Close"]),
        Decimal(data["Close"]),
        max_id_subquery,
        max_id_subquery,
    )
    execute_sql(
        """
        UPDATE test_transactions
        SET date_close = %s, close_price = %s, net_profit = %s - (SELECT open_price FROM test_transactions WHERE id = %s)
        WHERE id = %s
        """,
        params,
    )
