import pymysql as ps

from utils.config import DB_HOST, DB_INSTANCE_ID, DB__USER, DB_PASS


def get_connection():
    con = ps.connect(
        host=DB_HOST,
        user=DB__USER,
        password=DB_PASS,
        db=DB_INSTANCE_ID,
        charset="utf8mb4",
        cursorclass=ps.cursors.DictCursor,
    )
    return con
