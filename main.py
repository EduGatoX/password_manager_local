import auth
import db
import password as pw

from messages import Message, Messages
from models import MODELS

# DB engine to use: "sqlite3", ...
DB_ENGINE = "sqlite3"

# DB URL
DATABASE_URL = "password.db"


def greet():
    print(f"\n{'  WELCOME TO PASSWORD MANAGER  '::^50}\n")


def farewell():
    print(f"\n{'  Thank you for using our app  '::^50}")
    print(f"{'  Created by Eduardo Nuñez  '::^50}\n")


def main():
    """App entry point"""
    greet()

    # create db connection
    conn = db.DBConnectionFactory(DB_ENGINE, DATABASE_URL)

    # create connection
    conn.connect()

    # create tables based on the models
    for model in MODELS:
        conn.create_table(model)

    while True:
        # enter auth application
        response = auth.mainloop(conn)

        match response.message:
            case Messages.LOGIN_SUCCESS:
                # enter password manager application with authenticated user
                user = response.data
                pw.mainloop(conn, user)

            case Messages.QUIT:
                break
    farewell()


if __name__ == "__main__":
    main()
