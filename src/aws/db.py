from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from utils.logger import make_log
from utils.config import DATABASE_URI

engine = create_engine(DATABASE_URI, pool_size=10, max_overflow=20)


def execute_sql(sql, params=None):
    try:
        with engine.connect() as con:
            query = text(sql)
            result = con.execute(query, params) if params else con.execute(query)

            if sql.strip().lower().startswith("select"):
                columns = result.keys()

                sql_result = [dict(zip(columns, row)) for row in result]
                make_log(
                    "DB",
                    20,
                    "rds.log",
                    f"Executed: {sql, params} \n - \n Fetched: {sql_result} from RDS",
                )
                return sql_result
            else:
                make_log(
                    "DB",
                    20,
                    "rds.log",
                    f"Executed: {sql} \n - \n Affected: {rows_affected} rows",
                )
                return result.rowcount
    except SQLAlchemyError as e:
        make_log("DB", 40, "rds.log", f"Error executing SQL: {e}")
        return None
