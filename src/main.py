import app.dash_app as dsh
import aws.key as key
import aws.db as db


# def main():
#    dsh.run()


if __name__ == "__main__":
    print(db.get_connection())
