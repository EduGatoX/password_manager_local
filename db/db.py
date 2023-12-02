import sqlite3
from typing import Protocol

from .models import DBModel
from .types import SQLDataType


# TODO: I NEED TO SEPARATE MODELS FROM DB CONNECTIONS
# BY PASSING THE DATA TO THE DB CONNECTION AS A DICTIONARY
# OR OBJECT THAT IS ALREADY PARSED FROM THE MODEL USING AND
# ADAPTER PATTERN

# TODO: Maybe I need to return Messages from DBConnection to the client
# in order to test/verify the response of every method.

__TABLES__ = {
    "users": ["name", "email", "hashed_pw"],
    "passwords": ["app_name", "app_url", "username", "password","user_id"]
}


class DBConnection(Protocol):
    def create_connection(self):
        """Create the connection with the selected engine"""
        ...

    def create_table(self, table: str, columns: dict[str, str]):
        """Create a table according to the defined in the models module"""
        ...

    def insert_into_table(self, table: str, **data):
        """Insert 'data' into 'table'"""
        ...

    def select_all_from_table(self, table: str):
        """Select all the entries in 'table'"""
        ...

    def select_from_table_where(self, table: str, **kw):
        """Select all the entries from 'table' matching the conditions given by 'kw'"""
        ...

    def commit(self):
        """Commit changes of the current session"""
        ...

    def close_connection(self):
        """Close the connection"""
        ...


class SQLiteDBConnection:
    def __init__(self, url: str):
        self.url = url

    def create_connection(self):
        self.conn = sqlite3.connect(self.url)
        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

    def create_table(self, tablename: str, data: dict[str, SQLDataType]) -> None:
        if tablename not in __TABLES__:
            raise ValueError(f"Table {tablename} is not defined as a model.")
        
        sql = f"CREATE TABLE IF NOT EXISTS {tablename} ("
        sql += f"{', '.join([f"{column_name} {d_type.sql_type}" for column_name, d_type in data.items()])}"
        sql += ");"

        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            print(sql)

    def insert_into_table(self, table: str, model: DBModel) -> bool:
        if table not in __TABLES__:
            raise ValueError(f"Table '{table}' does not exist in the database")
        data = model.dump_data()
        sql = f"INSERT INTO {table} "
        sql += f"({', '.join(data.keys())}) "
        sql += f"VALUES ({', '.join(['?' for val in data.values()])});"
        cur = self.conn.cursor()
        print(sql)
        try:
            cur.execute(sql, tuple(data.values()))
            print(f"insert of {model} went ok")
            return True
        except Exception as e:
            print(e)
            print(f"insert of {model} went wrong")
            return False

    def select_all_from_table(self, table: str):
        if table not in __TABLES__:
            raise ValueError(f"Table '{table}' does not exist in the database")
        sql = f"SELECT * FROM {table}"
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)

    def select_from_table_where(self, table: str, **kw):
        if table not in __TABLES__:
            raise ValueError(f"Table '{table}' does not exist in the database")
        sql = f"SELECT * FROM {table} "
        sql += f"WHERE {', '.join([f'{k} = {v}' for k, v in kw.items()])};"
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            print(e)
            return None

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


def DBConnectionFactory(db_engine: str, db_url: str) -> DBConnection:
    match db_engine:
        case "sqlite3":
            return SQLiteDBConnection(db_url)
