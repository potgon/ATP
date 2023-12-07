import pymysql as ps
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
import os

from utils.logger import make_log
from utils.config import (
    RDS_PASSWORD,
    RDS_DB_NAME,
    RDS_HOSTNAME,
    RDS_PORT,
    RDS_USERNAME,
    EC2_INSTANCE,
    EC2_USER,
)


def create_db_engine():
    if os.getenv("ENV") == "PROD":
        DATABASE_URI = f"mysql+pymysql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}/{RDS_DB_NAME}"
    else:
        tunnel = SSHTunnelForwarder(
            (EC2_INSTANCE),
            ssh_username=EC2_USER,
            ssh_pkey="./aws/ATP-key.pem",
            remote_bind_address=(RDS_HOSTNAME, RDS_PORT),
        )
        tunnel.start()
        DATABASE_URI = f"mysql+pymysql://{RDS_USERNAME}:{RDS_PASSWORD}@localhost:{tunnel.local_bind_port}/{RDS_DB_NAME}"

    return create_engine(DATABASE_URI, pool_size=10, max_overflow=20)


def get_connection(tunnel: SSHTunnelForwarder):
    if os.getenv("ENV") == "PROD":
        return ps.connect(
            host=RDS_HOSTNAME,
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            port=RDS_PORT,
            database=RDS_DB_NAME,
        )
    else:
        return ps.connect(
            host="127.0.0.1",
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            port=tunnel.local_bind_port,
            database=RDS_DB_NAME,
        )


def execute_sql(sql, params=None):
    with SSHTunnelForwarder(
        ("ec2-3-251-101-46.eu-west-1.compute.amazonaws.com"),
        ssh_username="ec2-user",
        ssh_pkey="./aws/ATP-key.pem",
        remote_bind_address=(RDS_HOSTNAME, RDS_PORT),
    ) as tunnel:
        db = get_connection(tunnel)
        try:
            with db.cursor() as cur:
                cur.execute(sql, params)
                if sql.strip().lower().startswith("select"):
                    sql_result = [
                        tuple(str(item) for item in row) for row in cur.fetchall()
                    ]
                    make_log(
                        "RDS",
                        20,
                        "rds.log",
                        f"Executed {sql, params} \n and fetched {sql_result} from RDS",
                    )
                    return sql_result
                else:
                    rows_affected = cur.rowcount
                    db.commit()
                    make_log(
                        "RDS",
                        20,
                        "rds.log",
                        f"Executed {sql} in RDS, affected {rows_affected} rows",
                    )
                    return rows_affected
        finally:
            db.close()
