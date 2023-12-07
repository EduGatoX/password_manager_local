import sqlite3
from typing import Protocol, Any

from models.base import Table


class DBConnection(Protocol):
    def connect(self):
        """Create the connection with the selected engine"""

    def create_table(self, table: Table):
        """Create a new table named 'tablename'.

        Args:
            tablename (str) : The name of the new table.
            table (Table) : A class of type Table where its attributes are the
            column names for the SQL table.
        """

    def insert_into_table(self, tablename: str, data: dict[str, Any]):
        """Insert 'data' into the table named 'tablename'

        Args:
            tablename (str) : The name of the table.
            data (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns that are
                called in the insertion and (2) its values are regular python datatype values to be inserted for
                each column
        """

    def select_all_from_table(self, tablename: str) -> list[tuple[Any, ...]]:
        """Select all the entries from table called 'tablename'

        Args:
            tablename (str) : The name of the table.

        Return:
            A list with all the table entries. Each entry is a tuple containing the values
            for each column using basic python datatypes.
        """

    def select_from_table_where(self, tablename: str, conditions: dict[str, Any]) -> list[tuple[Any, ...]]:
        """Select all the entries from table named 'tablename' matching the conditions given by
        the dictionary 'conditions'

        Args:
            tablename (str) : The name of the table
            conditions (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns
                that are called in the selection and (2) its values are regular python datatype values that
                are part of the condition.

        Return:
            A list with all the table entries matching the conditions. Each entry is a tuple containing the values
            for each column using basic python datatypes.
        """

    def update_from_table_where(self, tablename: str, conditions: dict[str, Any], data: dict[str, Any]):
        """Update all the entries from table named 'tablename' matching the conditions given by the dictionary 'conditions'
        and replacing the values with the data inside 'data'.

        Args:
            tablename (str) : The name of the table
            conditions (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns
                that are called in the selection and (2) its values are regular python datatype values that
                are part of the condition.
            data (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns that are
                called in the update and (2) its values are regular python datatype values to be replaced for
                each column
        """

    def delete_from_table_where(self, tablename: str, conditions: dict[str, Any]):
        """Delete all the entries from table named 'tablename' matching the conditions given
        by the dictionary 'conditions'.

        Args:
            tablename (str) : The name of the table.
            conditions (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns
                that are called in the deletion and (2) its values are regular python datatype values that
                are part of the condition.
        """

    def commit(self):
        """Commit changes of the current session"""

    def close_connection(self):
        """Close the connection"""


class SQLiteDBConnection:
    def __init__(self, url: str):
        self.url = url

    def connect(self):
        self.conn = sqlite3.connect(self.url)
        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

    def create_table(self, table: Table) -> None:
        columns = list(table.__schema__.keys())
        contraints = [v.constraints for v in table.__schema__.values()]

        column_stmts = map(
            lambda item: f"{item[0]} {' '.join(item[1])}",
            zip(columns, contraints),
        )

        sql = f"CREATE TABLE IF NOT EXISTS {table.__tablename__} (\n\t"
        sql += f"{', \n\t'.join(list(column_stmts))}"
        sql += ");"

        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            print(sql)

    def insert_into_table(self, tablename: str, data: dict[str, Any]) -> None:
        columns, values = data.keys(), data.values()

        sql = f"INSERT INTO {tablename} \n"
        sql += f"({', '.join(columns)}) \n"
        sql += f"VALUES ({', '.join(['?' for _ in values])});"

        cur = self.conn.cursor()

        try:
            cur.execute(sql, list(values))
        except Exception as e:
            print(e)
            print(sql)

    def select_all_from_table(self, tablename: str) -> list[tuple[Any, ...]]:
        sql = f"SELECT * FROM {tablename};"

        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)

        return cur.fetchall()

    def select_from_table_where(self, tablename: str, conditions: dict[str, Any]) -> list[tuple[Any, ...]]:
        columns = list(conditions.keys())
        values = list(conditions.values())

        sql = f"SELECT * FROM {tablename} \n\t"
        sql += f"WHERE {', \n\t'.join([f'{k} = ?' for k in columns])};"

        cur = self.conn.cursor()
        try:
            cur.execute(sql, values)
            return cur.fetchall()
        except Exception as e:
            print(e)
            return None

    def update_from_table_where(self, tablename: str, conditions: dict[str, Any], data: dict[str, Any]):
        new_values = list(data.values())
        condition_values = list(conditions.values())

        sql = f"UPDATE {tablename} \n"
        sql += f"SET {', \n\t'.join([f'{k} = ?' for k in data.keys()])} \n"
        sql += f"WHERE {', \n\t'.join([f'{k} = ?' for k in conditions.keys()])};"

        cur = self.conn.cursor()
        try:
            cur.execute(sql, [*new_values, *condition_values])
        except Exception as e:
            print(e)
            print(sql)

    def delete_from_table_where(self, tablename: str, conditions: dict[str, Any]):
        values = list(conditions.values())

        sql = f"DELETE FROM {tablename} \n"
        sql += f"WHERE {', \n\t'.join([f'{k} = ?' for k in conditions.keys()])};"

        cur = self.conn.cursor()
        try:
            cur.execute(sql, values)
        except Exception as e:
            print(e)
            print(sql)

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


def DBConnectionFactory(db_engine: str, db_url: str) -> DBConnection:
    match db_engine:
        case "sqlite3":
            return SQLiteDBConnection(db_url)
