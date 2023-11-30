import bcrypt
from getpass import getpass

import db
from helper import Option, index, choice
from messages import Messages, Message


def validate_password(plain_pw: str, hashed_pw: bytes) -> bool:
    return bcrypt.checkpw(plain_pw.encode("utf8"), hashed_pw)


def login(conn: db.DBConnection) -> Message[db.models.User]:
    print(f"\n{'  LOGIN  '::^50}\n")
    email: str = input(f"{'Enter your email: ':<25}")
    password: str = input(f"{'Enter your password: ':<25}")

    if not validate_password(password, user.hashed_pw):
        print("Invalid credentials. Try Again.")
        return Message(Messages.LOGIN_FAILURE, None)

    data = conn.select_from_table_where("users", email=email)
    user = db.models.User(**data)


def sign_up(conn: db.DBConnection) -> Message[None]:
    print(f"\n{'  SIGN UP  '::^50}\n")
    name: str = input(f"{'Enter your name: ':<25}")
    email: str = input(f"{'Enter your email: ':<25}")
    plain_pw: str = getpass(f"{'Enter password: ':<25}")
    confirm_pw: str = getpass(f"{'Confirm password: ':<25}")

    if plain_pw != confirm_pw:
        print("Passwords don't match. Try again.")
        return sign_up(conn)

    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(plain_pw.encode("utf8"), salt)

    user = db.models.User("", name, email, str(hashed_pw))

    if not conn.insert_into_table("users", user):
        print(f"\nUser {user.email} couldn't be saved. Try again later\n")
        return Message(Messages.SIGN_UP_FAILURE, None)

    print(f"\nUser {user.email} saved successfully. Please, log in.\n")
    return Message(Messages.SIGN_UP_SUCCESS, None)


def mainloop(conn: db.DBConnection) -> Message[db.models.User | None]:
    print(f"\n{'  AUTHENTICATION  '::^50}\n")
    options = [
        Option("Login", login),
        Option("Sign Up", sign_up),
        Option("Quit", lambda _: Message(Messages.QUIT, None)),
    ]

    index(options)
    option = choice(options)

    response = option.func(conn)

    return response
