import app.dash_app as dsh
import aws.db as db


def main():
    dsh.run()


# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    db.get_ssh_con("SHOW TABLES;")
