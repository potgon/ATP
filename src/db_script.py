from aws.db import execute_sql
from app.dash_app import retrieve_fetcher
from app.snr import calculate_reversal_zones

fetcher = retrieve_fetcher()


def check_sql(sql: str):
    execute_sql(sql)


def insert_asset(sql) -> None:
    execute_sql(sql)


def insert_zone() -> None:
    with fetcher.data_lock:
        data = fetcher.current_data.copy()

    avg_price = data["Close"].mean()
    valid_zones = calculate_reversal_zones(avg_price)

    for idx, row in valid_zones.iterrows():
        sql = f"INSERT INTO reversal_zones (asset_id, price, zone_type, price_range_max, price_range_min) VALUES ((SELECT id FROM assets WHERE name = '{fetcher.ticker}'),{row['Price']},'{row['Type']}',{row['Max']},{row['Min']});"
        execute_sql(sql)


if __name__ == "__main__":
    insert_zone()
