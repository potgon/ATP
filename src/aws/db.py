import pymysql as ps
from sshtunnel import SSHTunnelForwarder

from utils.config import (
    RDS_PASSWORD,
    RDS_DB_NAME,
    RDS_HOSTNAME,
    RDS_PORT,
    RDS_USERNAME,
    EC2_KEY,
)


def get_connection():
    con = ps.connect(
        host=RDS_HOSTNAME, user=RDS_USERNAME, password=RDS_PASSWORD, db=RDS_DB_NAME
    )

    try:
        with con.cursor() as cursor:
            sql = "SELECT VERSION()"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)

        con.commit()
    finally:
        con.close()


def get_ssh_con():
    with SSHTunnelForwarder(
        ("ec2-34-250-215-95.eu-west-1.compute.amazonaws.com"),
        ssh_username="ec2-user",
        ssh_pkey=EC2_KEY,
        remote_bind_address=(RDS_HOSTNAME, RDS_PORT),
    ) as tunnel:
        print("Tunnel Established")

        db = ps.connect(
            host="127.0.0.1",
            user=RDS_USERNAME,
            password=RDS_PASSWORD,
            port=tunnel.local_bind_port,
            database=RDS_DB_NAME,
        )

        try:
            with db.cursor() as cur:
                cur.execute(
                    """CREATE TABLE `users` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `email` varchar(255) COLLATE utf8_bin NOT NULL,
                        `password` varchar(255) COLLATE utf8_bin NOT NULL,
                        PRIMARY KEY (`id`)
                        )
                        AUTO_INCREMENT=1;"""
                )

                cur.execute("SHOW TABLES;")
                for r in cur:
                    print(r)
        finally:
            db.close()
