import pymysql as ps

from utils.logger import make_log
from utils.config import (
    RDS_PASSWORD,
    RDS_DB_NAME,
    RDS_HOSTNAME,
    RDS_PORT,
    RDS_USERNAME,
)


def get_connection():
    return ps.connect(
        host=RDS_HOSTNAME,
        user=RDS_USERNAME,
        password=RDS_PASSWORD,
        port=RDS_PORT,
        database=RDS_DB_NAME,
    )


def execute_sql(sql):
    db = get_connection()

    try:
        with db.cursor() as cur:
            cur.execute(sql)
            sql_result = [str(r[0]) for r in cur]
            db.commit()
    finally:
        db.close()
    make_log("RDS", 20, "workflow.log", f"Fetched {sql_result} from RDS")
    return sql_result
