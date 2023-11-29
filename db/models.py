from typing import Protocol
from dataclasses import dataclass


class DBModel(Protocol):
    @classmethod
    def create_table_sql(cls) -> str:
        ...

    def dump_data(self) -> dict[str, str]:
        ...


@dataclass
class User:
    user_id: str
    name: str
    email: str
    hashed_pw: str

    @classmethod
    def create_table_sql(cls) -> str:
        sql = "CREATE TABLE IF NOT EXISTS users "
        sql += "(user_id INTEGER PRIMARY KEY, "
        sql += "name TEXT NOT NULL, "
        sql += "email TEXT NOT NULL UNIQUE, "
        sql += "hashed_pw TEXT NOT NULL);"
        return sql

    def dump_data(self) -> dict[str, str]:
        data = dict(self.__dict__)
        del data["user_id"]
        return data

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name}, email={self.email})"


@dataclass
class Password:
    password_id: str
    app_name: str
    app_url: str
    username: str
    password: str
    user_id: str

    @classmethod
    def create_table_sql(cls) -> str:
        sql = "CREATE TABLE IF NOT EXISTS passwords "
        sql += "(password_id INTEGER PRIMARY KEY, "
        sql += "app_name TEXT NOT NULL, "
        sql += "app_url TEXT NOT NULL UNIQUE, "
        sql += "username TEXT NOT NULL, "
        sql += "password TEXT NOT NULL, "
        sql += "user_id INTEGER NOT NULL, "
        sql += "FOREIGN KEY (user_id) REFERENCES users (user_id));"

        return sql

    def dump_data(self):
        data = dict(self.__dict__)
        del data["password_id"]
        return data

    def __repr__(self):
        result = f"User(name={self.app_name}, url={self.app_name}, "
        result += f"username={self.username}, password={self.password})"
        return result
