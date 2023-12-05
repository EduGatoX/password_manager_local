"""Create your models here by following the next steps.

1) Import TableModel from ./models/base.py

2) Create one class for each table you want to add to the Database and each
one should inherit from TableModel.

3) Once you create these classes, each class should have an attribute called
__tablename__ of type str, where you should put the name of the table you want
to use for it in the database.

4) Finally, create all the attributes you want of type SQLDataType (Integer, Text
Float or NullType). You should select one as a primary key.
"""

from .base import TableModel
from .typing import SQLDataType, Integer, Text, Float, NullType


class User(TableModel):
    __tablename__ = "users"

    user_id: SQLDataType = Integer("sqlite3", primary_key=True, unique=True)
    name: SQLDataType = Text("sqlite3", False)
    email: SQLDataType = Text("sqlite3", False)
    hashed_pw: SQLDataType = Text("sqlite3", False)


class Password(TableModel):
    __tablename__ = "passwords"

    password_id: SQLDataType = Integer("sqlite3", primary_key=True, unique=True)
    app_name: SQLDataType = Text("sqlite3", nullable=False)
    app_url: SQLDataType = Text("sqlite3", nullable=False, unique=True)
    username: SQLDataType = Text("sqlite3", nullable=False, unique=True)
    password: SQLDataType = Text("sqlite3", nullable=False)
