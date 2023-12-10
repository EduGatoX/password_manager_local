import sqlite3
from typing import Protocol, Any

from models.base import Table


class DBConnection(Protocol):
    def connect(self) -> None:
        """Create the connection with the selected engine"""

    def create_table(self, table: Table) -> str:
        """Return the sql statement for create table define by the model 'table'.

        Args:
            table (Table) : A class of type Table

        Return:
            The sql statement for creating the new table
        """

    def insert_into_table(self, table: Table) -> str:
        """Return the sql statement for inserting 'data' into the 'table'.

        Args:
            table (Table) : A class of type Table

        Return:
            The sql statement for inserting 'data'
        """

    def select_all_from_table(self, table: Table) -> str:
        """Return the sql statement for selecting all the entries from 'table'.

        Args:
            table (Table) : A class of type Table

        Return:
            The sql statement for selecting all the entries from 'table'
        """

    def select_from_table_where(self, table: Table, conditions: dict[str, Any]) -> str:
        """Return the sql statement for selecting all the entries from table named 'tablename' matching the conditions given by
        the dictionary 'conditions'

        Args:
            table (Table) : A class of type Table
            conditions (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns
                that are called in the selection and (2) its values are regular python datatype values that
                are part of the condition.

        Return:
            The sql statement for selecting all the entries from 'table' matching the conditions given by
            the dictionary 'conditions'
        """

    def update_from_table_where(self, table: Table, conditions: dict[str, Any], data: dict[str, Any]) -> str:
        """Return the sql statement for updating all the entries from 'table' matching the conditions given 
        by the dictionary 'conditions' and replacing them with the values inside 'data'.

        Args:
            table (Table) : A class of type Table
            conditions (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns
                that are called in the selection and (2) its values are regular python datatype values that
                are part of the condition.
            data (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns that are
                called in the update and (2) its values are regular python datatype values to be replaced for
                each column

        Return:
            The sql statement for updating all the entries from 'table' matching the conditions given 
            by the dictionary 'conditions' and replacing them with the values inside 'data'
        """

    def delete_from_table_where(self, table: Table, conditions: dict[str, Any]) -> str:
        """Return the sql statement for deleting all the entries from 'table' matching the conditions given
        by the dictionary 'conditions'.

        Args:
            table (Table) : A class of type Table
            conditions (dict[str, Any]) : A dictionary where (1) its keys represent the names of the columns
                that are called in the deletion and (2) its values are regular python datatype values that
                are part of the condition.

        Return:
            The sql statement for deleting all the entries from 'table' matching the conditions given
            y the dictionary 'conditions'.
        """

    def execute(self, sql: str, parameters: tuple[Any, ...] = ()) -> list[Any]:
        """Execute the sql statement with the parameters given in the arguments.

        Args:
            sql (str) : The sql statement.
            parameters (tuple[Any, ...]) : The parameters that will be replaced in the sql statement placeholders.

        Return:
            A list with the data requested in the sql statement or an empty list if no data was requested in the sql statement
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

    def create_table(self, table: Table) -> str:
        columns = list(table.__schema__.keys())
        d_types = [v.d_type for v in table.__schema__.values()]
        contraints = [v.constraints for v in table.__schema__.values()]

        column_stmts = map(
            lambda item: f"{item[0]} {item[1]} {' '.join(item[2])}",
            zip(columns, d_types, contraints),
        )

        sql = f"CREATE TABLE IF NOT EXISTS {table.__tablename__} (\n\t"
        sql += f"{', \n\t'.join(list(column_stmts))}"
        sql += ");"

        return sql

    def insert_into_table(self, table: Table) -> str:

        filtered_dict = dict(filter(lambda item: not item[1].primary_key,
                                    table.__schema__.items()))

        columns = list(filtered_dict.keys())

        sql = f"INSERT INTO {table.__tablename__} \n"
        sql += f"({', '.join(columns)}) \n"
        sql += f"VALUES ({', '.join(['?' for _ in columns])});"

        return sql

    def select_all_from_table(self, table: Table) -> str:
        sql = f"SELECT * FROM {table.__tablename__};"

        return sql

    def select_from_table_where(self, table: Table, conditions: dict[str, Any]) -> str:
        columns = list(conditions.keys())

        sql = f"SELECT * FROM {table.__tablename__} \n\t"
        sql += f"WHERE {', \n\t'.join([f'{k} = ?' for k in columns])};"

        return sql

    def update_from_table_where(self, table: Table, conditions: dict[str, Any], data: dict[str, Any]) -> str:
        sql = f"UPDATE {table.__tablename__} \n"
        sql += f"SET {', \n\t'.join([f'{k} = ?' for k in data.keys()])} \n"
        sql += f"WHERE {', \n\t'.join([f'{k} = ?' for k in conditions.keys()])};"

        return sql

    def delete_from_table_where(self, table: Table, conditions: dict[str, Any]) -> str:
        sql = f"DELETE FROM {table.__tablename__} \n"
        sql += f"WHERE {', \n\t'.join([f'{k} = ?' for k in conditions.keys()])};"

        return sql

    def execute(self, sql: str, parameters: tuple[Any, ...] = ()) -> list[Any]:
        try:
            cur = self.conn.cursor()
            cur.execute(sql, parameters)
            return cur.fetchall()
        except Exception as e:
            print(e)
            print(sql)
            return []

    def commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


def DBConnectionFactory(db_engine: str, db_url: str) -> DBConnection:
    match db_engine:
        case "sqlite3":
            return SQLiteDBConnection(db_url)
