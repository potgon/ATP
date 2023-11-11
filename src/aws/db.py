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


def get_ssh_con(sql):
    with SSHTunnelForwarder(
        ("ec2-34-250-215-95.eu-west-1.compute.amazonaws.com"),
        ssh_username="ec2-user",
        ssh_pkey="./aws/ATP-key.pem",
        remote_bind_address=(RDS_HOSTNAME, RDS_PORT),
    ) as tunnel:
        make_log("RDS", 10, "db.log", "Tunnel Established")

        db = get_connection(tunnel)

        try:
            with db.cursor() as cur:
                cur.execute(sql)
                for r in cur:
                    make_log("RDS", 20, "db.log", r)
        finally:
            db.close()
