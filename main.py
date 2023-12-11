import auth
import db
import password as pw

from messages import Message, Messages
from models import MODELS

# Important: First check config.py if DB_ENGINE and DATABASE_URL
# are defined.
from config import DB_ENGINE, DATABASE_URL


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
        sql = conn.create_table(model)
        conn.execute(sql)

    while True:
        # enter auth application
        response: Message = auth.mainloop(conn)

        match response.message:
            case Messages.LOGIN_SUCCESS:
                # enter password manager application with authenticated user
                user = response.data
                print(user)
                print(response.message)
                # pw.mainloop(conn, user)

            case Messages.QUIT:
                break
    farewell()


if __name__ == "__main__":
    main()
