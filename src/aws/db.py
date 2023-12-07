from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from utils.logger import make_log
from utils.config import DATABASE_URI

engine = create_engine(DATABASE_URI, pool_size=10, max_overflow=20)


def execute_sql(sql, params=None):
    try:
        with engine.connect() as con:
            result = con.execute(sql, params)
            if sql.strip().lower().startswith("select"):
                sql_result = [dict(row) for row in result]
                make_log(
                    "RDS",
                    20,
                    "rds.log",
                    f"Executed {sql, params} \n and fetched {sql_result} from RDS",
                )
                return sql_result
            else:
                rows_affected = con.rowcount
                make_log(
                    "RDS",
                    20,
                    "rds.log",
                    f"Executed {sql} in RDS, affected {rows_affected} rows",
                )
                return rows_affected
    except SQLAlchemyError as e:
        make_log("RDS", 40, "rds.log", f"Error executing SQL: {e}")
