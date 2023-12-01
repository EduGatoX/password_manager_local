from .types import SQLDataType, Integer, Text
from typing import Protocol
from dataclasses import dataclass


class DBModel(Protocol):
    def dump_data(self) -> dict[str, SQLDataType]:
        ...


@dataclass
class User:
    user_id: Integer
    name: Text
    email: Text
    hashed_pw: Text

    def dump_data(self) -> dict[str, SQLDataType]:
        data = dict(self.__dict__)
        del data["user_id"]
        return data

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name}, email={self.email})"


@dataclass
class Password:
    password_id: Integer
    app_name: Text
    app_url: Text
    username: Text
    password: Text
    user_id: Text

    def dump_data(self) -> dict[str, SQLDataType]:
        data = dict(self.__dict__)
        del data["password_id"]
        return data

    def __repr__(self):
        result = f"Password(name={self.app_url}, username={self.username}, password={self.password})"
        return result
