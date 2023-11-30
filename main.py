import auth
import db
import password as pw

from messages import Message, Messages

# DB engine to use: "sqlite", ...
DB_ENGINE = "sqlite"

# DB URL
DATABASE_URL = "password.db"

# create new models in db.models and then put them here in the list
# as a type
MODELS = [db.models.User, db.models.Password]


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
    conn.create_connection()

    # create tables based on the models
    conn.create_tables(MODELS)

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
