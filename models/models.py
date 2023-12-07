"""Create your models here by following the next steps.

1) Import TableModel from ./models/base.py

2) Create one class for each table you want to add to the Database and each
one should inherit from TableModel.

3) Once you create these classes, each class should have an attribute called
__tablename__ of type str, where you should put the name of the table you want
to use for it in the database.

4) Create all the attributes you want of type SQLDataType (Integer, Text
Float or NullType). You should select one as a primary key.

5) Finally, add the models to the list MODELS at the end of this module.
"""

from .base import Table, TableModel
from .typing import SQLDataType, Integer, Text, Float, NullType
from typing import Any

# Create your models here


class User(TableModel):
    __tablename__ = "users"

    user_id: SQLDataType = Integer("sqlite3", primary_key=True, unique=True)
    name: SQLDataType = Text("sqlite3", False)
    email: SQLDataType = Text("sqlite3", False)
    hashed_pw: SQLDataType = Text("sqlite3", False)


class Password(TableModel):
    __tablename__ = "passwords"

    password_id: SQLDataType = Integer("sqlite3", primary_key=True,
                                       unique=True)
    app_name: SQLDataType = Text("sqlite3", nullable=False)
    app_url: SQLDataType = Text("sqlite3", nullable=False, unique=True)
    username: SQLDataType = Text("sqlite3", nullable=False, unique=True)
    password: SQLDataType = Text("sqlite3", nullable=False)


# Add the created models
MODELS = [User, Password]


def validate_data(table: Table, data: dict[str, Any]) -> bool:
    """Validates 'data' against 'table' so that it respects the schema defined by the model.

    Args:
        table (Table) : A table model as defined in this module.
        data (data[str, Any]) : data to be validated against the model.

    Return:
        True if 'data' is successfully validated and False if not.
    """
    table_schema = table.__schema__
    # Check if keys exist in the table
    for key in data:
        if key not in table_schema:
            return False

    # Check type of values
    for key, value in data.items():
        sql_data_type = table_schema.get(key, NullType("sqlite3"))
        if not isinstance(value, sql_data_type.py_type):
            return False

    for key, value in table_schema.items():
        # Check primary key (it shouldn't be part of data)
        if value.primary_key and key in data:
            return False
        elif value.primary_key and key not in data:
            continue
        # Check nullability
        if not value.nullable and key not in data:
            return False
        # TODO: Check uniqueness (HOW? Probably we should leave that to the DBConnection)

    return True
