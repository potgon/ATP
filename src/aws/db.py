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


def execute_sql(sql, params=None):
    db = get_connection()
    try:
        with db.cursor() as cur:
            cur.execute(sql, params)
            if sql.lower().startswith("select"):
                sql_result = [str(r[0]) for r in cur]
                make_log("RDS", 20, "workflow.log", f"Fetched {sql_result} from RDS")
                return sql_result
            else:
                rows_affected = cur.rowcount
                db.commit()
                make_log(
                    "RDS",
                    20,
                    "workflow.log",
                    f"Executed {sql} in RDS, affected {rows_affected} rows",
                )
                return rows_affected
    finally:
        db.close()
