import sqlite3
from typing import Protocol, Any

from .types import SQLDataType


# TODO: I NEED TO SEPARATE MODELS FROM DB CONNECTIONS
# BY PASSING THE DATA TO THE DB CONNECTION AS A DICTIONARY
# OR OBJECT THAT IS ALREADY PARSED FROM THE MODEL USING AND
# ADAPTER PATTERN

# TODO: I need to find a way to not depend on SQLDataType and instead
# pass regular python types (maybe pass a dictionary instead of SQLDataType)

# TODO: Maybe I need to return Messages from DBConnection to the client
# in order to test/verify the response of every method.

__TABLES__ = {
    "users": ["name", "email", "hashed_pw"],
    "passwords": ["app_name", "app_url", "username", "password", "user_id"],
}


class DBConnection(Protocol):
    def create_connection(self):
        """Create the connection with the selected engine"""

    def create_table(self, tablename: str, columns: dict[str, SQLDataType]):
        """Create a new table named 'tablename'.

        Args:
            tablename (str) : The name of the new table.
            columns (dict[str, SQLDataType]) : A dictionary where (1) its keys represent the
                name of the columns of the new table and (2) its values represent the data type
                of each column (use SQLDataType of module db/types.py)
        """

    def insert_into_table(self, tablename: str, data: dict[str, SQLDataType]):
        """Insert 'data' into the table named 'tablename'

        Args:
            tablename (str) : The name of the table.
            data (dict[str, SQLDataType]) : A dictionary where (1) its keys represent the
                names of the columns that are called in the insertion and (2) its values are objects of type
                SQLDataType that contain the sql data type and the value to be inserted for each column
                (use SQLDataType of module db/types.py)
        """

    def select_all_from_table(self, tablename: str) -> list[tuple[Any, ...]]:
        """Select all the entries from table called 'tablename'

        Args:
            tablename (str) : The name of the table.

        Return:
            A list with all the table entries. Each entry is a tuple containing the values
            for each column using basic python datatypes.
        """

    def select_from_table_where(self, tablename: str, conditions: dict[str, SQLDataType]) -> list[tuple[Any, ...]]:
        """Select all the entries from table named 'tablename' matching the conditions given by
        the dictionary 'conditions'

        Args:
            tablename (str) : The name of the table
            conditions (dict[str, SQLDataType]) : A dictionary where (1) its keys represent the
                names of the columns that are called in the insertion and (2) its values are objects of type
                SQLDataType that contain the sql data type and the value that is part of the condition for
                the respecting column (use SQLDataType of module db/types.py)

        Return:
            A list with all the table entries matching the conditions. Each entry is a tuple containing the values
            for each column using basic python datatypes.
        """

    def commit(self):
        """Commit changes of the current session"""

    def close_connection(self):
        """Close the connection"""


class SQLiteDBConnection:
    def __init__(self, url: str):
        self.url = url

    def create_connection(self):
        self.conn = sqlite3.connect(self.url)
        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

    def create_table(self, tablename: str, columns: dict[str, SQLDataType]) -> None:
        if tablename not in __TABLES__:
            raise ValueError(f"Table {tablename} is not defined as a model.")

        column_type_stmts = [f"{column_name} {d_type.sql_type}" for column_name, d_type in columns.items()]

        sql = f"CREATE TABLE IF NOT EXISTS {tablename} ("
        sql += f"{', '.join(column_type_stmts)}"
        sql += ");"

        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            print(sql)

    def insert_into_table(self, tablename: str, data: dict[str, SQLDataType]) -> None:
        if tablename not in __TABLES__:
            raise ValueError(f"Table '{tablename}' does not exist in the database")

        # Extract values from data and assign to None the column that is primary key
        column_value_stmts = [
            (None, None) if d_type.primary_key else (column, d_type.value) for column, d_type in data.items()
        ]

        # Filter the previous list and take out the None values in order to not
        # add the primary key (because it is automatically added by the engine)
        filtered_column_value_stmts = list(filter(lambda x: all(x), column_value_stmts))
        columns, values = tuple(zip(*filtered_column_value_stmts))

        sql = f"INSERT INTO {tablename} \n"
        sql += f"({', '.join(columns)}) \n"
        sql += f"VALUES ({', '.join(['?' for val in values])});"

        cur = self.conn.cursor()

        try:
            cur.execute(sql, values)
        except Exception as e:
            print(e)
            print(sql)

    def select_all_from_table(self, tablename: str) -> list[tuple[Any, ...]]:
        if tablename not in __TABLES__:
            raise ValueError(f"Table '{tablename}' does not exist in the database")

        sql = f"SELECT * FROM {tablename};"

        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)

        return cur.fetchall()

    def select_from_table_where(self, tablename: str, conditions: dict[str, SQLDataType]) -> list[tuple[Any, ...]]:
        if tablename not in __TABLES__:
            raise ValueError(f"Table '{tablename}' does not exist in the database")

        condition_values = [f"{v.value}" for v in conditions.values()]

        sql = f"SELECT * FROM {tablename} \n\t"
        sql += f"WHERE {', \n\t'.join([f'{k} = ?' for k, _ in conditions.items()])};"
        
        cur = self.conn.cursor()
        try:
            cur.execute(sql, condition_values)
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
