import bcrypt
from getpass import getpass
from typing import Any

import db
from models.base import Table
from models.models import User
from helper import Option, index, choice
from messages import Messages, Message


def validate_password(plain_pw: str, hashed_pw: str) -> bool:
    return bcrypt.checkpw(plain_pw.encode("utf8"), hashed_pw.encode("utf8"))


def hash_password(plain_pw: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_pw.encode("utf8"), salt).decode("utf8")


def params_exist(conn: db.DBConnection, table: Table, **params: dict[str, Any]) -> bool:
    sql = conn.select_from_table_where(table, params)
    result = conn.execute(sql, tuple(params.values()))
    return result != []


def create_user_dict_from_tuple(user_id: int, name: str, email: str, hashed_pw: str):
    return dict(user_id=user_id, name=name,
                email=email, hashed_pw=hashed_pw)


def login(conn: db.DBConnection) -> Message:
    print(f"\n{'  LOGIN  '::^50}\n")
    email: str = input(f"{'Enter your email: ':<25}")
    password: str = getpass(f"{'Enter your password: ':<25}")

    sql = conn.select_from_table_where(User, dict(email=email))
    result: list[tuple[Any, ...]] = \
        conn.execute(sql, parameters=(email,))

    # unpack the first (and only) element of the list result
    user = create_user_dict_from_tuple(*result[0])

    if not validate_password(password, user["hashed_pw"]):
        print("Invalid credentials. Try Again.")
        return Message(Messages.LOGIN_FAILURE, None)

    return Message(Messages.LOGIN_SUCCESS, user)


def sign_up(conn: db.DBConnection) -> Message:
    print(f"\n{'  SIGN UP  '::^50}\n")
    name: str = input(f"{'Enter your name: ':<25}")
    email: str = input(f"{'Enter your email: ':<25}")
    plain_pw: str = getpass(f"{'Enter password: ':<25}")
    confirm_pw: str = getpass(f"{'Confirm password: ':<25}")

    if params_exist(conn, User, email=email):
        print("\nEmail is already registered. Please, try again.")
        return Message(Messages.SIGN_UP_FAILURE, None)

    if plain_pw != confirm_pw:
        print("\nPasswords don't match. Please, try again.")
        return sign_up(conn)

    hashed_pw = hash_password(plain_pw)

    user = dict(name=name, email=email, hashed_pw=hashed_pw)

    if not User.validate_data(user):
        print("\nData entered is invalid. Please, try again.")
        return Message(Messages.SIGN_UP_FAILURE, None)

    sql = conn.insert_into_table(User)
    values = tuple(user.values())
    result = conn.execute(sql, values)

    conn.commit()

    print(f"\nUser {user["name"]} saved successfully. Please, log in.\n")

    return Message(Messages.SIGN_UP_SUCCESS, result)


def mainloop(conn: db.DBConnection) -> Message:
    print(f"\n{'  AUTHENTICATION  '::^50}\n")
    options = [
        Option("Login", login),
        Option("Sign Up", sign_up),
        Option("Quit", lambda _: Message(Messages.QUIT, None)),
    ]

    index(options)
    option = choice(options)

    if not option:
        print("Invalid input. Please try again.")
        return mainloop(conn)

    response = option.func(conn)

    return response
