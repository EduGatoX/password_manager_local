import bcrypt
from getpass import getpass

import db
from helper import Option, index, choice
from messages import Messages, Message


def print_all_passwords(conn: db.DBConnection, user: db.models.User):
    passwords = conn.select_from_table_where("password", user_id=user.user_id)
    for password in passwords:
        print(password)


def print_password_by_url(conn: db.Connection, user: db.models.User):
    url = input(f"{'Enter url':<25}")
    password = conn.select_from_table_where("password", user_id=user.user_id, url=url)
    print(password)


def mainloop(conn: db.DBConnection, user: db.models.User) -> Message:
    print(f"\n{'  AUTHENTICATION  '::^50}\n")
    options = {
        "1": Option("Print all passwords", print_all_passwords),
        "2": Option("Print password by url", print_password_by_url),
        "3": Option("Logout", lambda _: Message(Messages.LOGOUT, None)),
    }

    index(options)
    option: Option = choice(options)

    response: Message = option.func(conn, user)

    return response
