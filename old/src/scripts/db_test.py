from sqlalchemy import create_engine, text
from utils.config import DATABASE_URI


def test_database_connection():
    engine = create_engine(DATABASE_URI)

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            version = result.fetchone()
            print("Database connection test successful. MySQL version:",
                  version[0])
            return True
    except Exception as e:
        print("Database connection test failed:", e)
        return False


if __name__ == "__main__":
    if test_database_connection():
        print("Connection to database established successfully.")
    else:
        print("Failed to establish connection to the database.")
