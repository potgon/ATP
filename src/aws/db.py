import pymysql as ps
from sshtunnel import SSHTunnelForwarder

from utils.logger import make_log
from utils.config import (
    RDS_PASSWORD,
    RDS_DB_NAME,
    RDS_HOSTNAME,
    RDS_PORT,
    RDS_USERNAME,
)


def get_connection(tunnel: SSHTunnelForwarder):
    return ps.connect(
        host="127.0.0.1",
        user=RDS_USERNAME,
        password=RDS_PASSWORD,
        port=tunnel.local_bind_port,
        database=RDS_DB_NAME,
    )


def execute_sql(sql):
    with SSHTunnelForwarder(
        ("ec2-3-251-101-46.eu-west-1.compute.amazonaws.com"),
        ssh_username="ec2-user",
        ssh_pkey="./aws/ATP-key.pem",
        remote_bind_address=(RDS_HOSTNAME, RDS_PORT),
    ) as tunnel:
        db = get_connection(tunnel)

        try:
            with db.cursor() as cur:
                cur.execute(sql)
                sql_result = [str(r[0]) for r in cur]
                db.commit()
        finally:
            db.close()
    make_log("RDS", 20, "workflow.log", f"Fetched {sql_result} from RDS")
    return sql_result
