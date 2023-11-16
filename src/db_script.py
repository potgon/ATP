from aws.db import execute_sql
from app.fetcher import Fetcher

fetcher: Fetcher = Fetcher("EURUSD=X")


def check_sql(sql: str):
    execute_sql(sql)


def insert_asset(sql) -> None:
    execute_sql(sql)


def insert_support() -> None:
    with fetcher.data_lock:
        data = fetcher.current_data.copy()

    unique_supports = data["Support"].dropna().unique()

    for support in unique_supports:
        sql = f"INSERT INTO supports (asset_id, price) VALUES ((SELECT id FROM assets WHERE name = '{fetcher.ticker}'), {support});"
        execute_sql(sql)


def insert_resistance() -> None:
    with fetcher.data_lock:
        data = fetcher.current_data.copy()

    unique_resistances = data["Resistance"].dropna().unique()

    for resistance in unique_resistances:
        sql = f"INSERT INTO resistances (asset_id, price) VALUES ((SELECT id FROM assets WHERE name = '{fetcher.ticker}'), {resistance});"
        execute_sql(sql)


if __name__ == "__main__":
    check_sql("SELECT * FROM supports;")
