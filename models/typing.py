"""
This module contains the bindings between python types and sql types

To add a new engine, follow the next steps.

1. Create a new dictionary of type bindings between python types and SQL types of the desired engine.
Each item in the dictionary should follow the example: (int : 'INTEGER'). In this example 'int' is the python type
given as a key, and 'INTEGER' is the str representation of the SQL datatype the match the python type 'int'.

2. Create a new dictionary of constraints of the desired SQL engine. Constraints are restrictions for data inside
the database engine that should be respected when entering new data. For example, NOT NULL in sqlite3 means that
the data entered in the respective column should be a NOT NULL value. Other example is UNIQUE in sqlite3, that means
that every entry in that column should be entered only once.

Each item in the dictionary should follow the example: ('not_null': 'NOT NULL'), where 'not null' is the key that is used in
tge definition of SQLDataType and 'NOT NULL' is the sqlite3 str representation of the contraint.

At the moment there are 3 constraints supported, those are 'not_null', 'primary_key' and 'unique'.

3. Add the bindings between the database engine and the type bindings in the TYPE_BINDINGS dictionary. The
binding should follow the example: ("sqlite3": sqlite_type_binding) where the str "sqlite3" is the key that
should be provided in config.py as part of the constant DB_ENGINE. sqlite_type_binding is the dictionary created
in step 1 (in this case for the 'sqlite3' engine)

4. Add the bindings between the database engine and the sql_constraints in the SQL_CONSTRAINTS dictionary. The binding
should follow the example ('sqlite3' : sqlite_constraints) where 'sqlite3' is the DB_ENGINE that should be provided in config.py
and sqlite_constraints is the dictionary created in step 2 (in this case for 'sqlite3' engine)
"""

from __future__ import annotations
from config import DB_ENGINE

# Create your bindings here

# sqlite type bindings
sqlite_type_binding = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    None: "NULL",
}

# sqlite type constraints
sqlite_constraints = {
    "not_null": "NOT NULL",
    "primary_key": "PRIMARY KEY",
    "unique": "UNIQUE",
}

# Create your bindings here

# Relationship between engines and type relationships
TYPE_BINDINGS = {
    "sqlite3": sqlite_type_binding,
}

# Relationship between engines and type constraints
SQL_CONSTRAINTS = {
    "sqlite3": sqlite_constraints,
}


class SQLDataType:
    def __init__(self, py_type: type, nullable: bool = True,
                 primary_key: bool = False, unique: bool = False):
        self.db_engine = DB_ENGINE
        self.py_type = py_type

        if primary_key:
            # primary_key overrides nullable and unique attributes
            self.primary_key = primary_key
            self.nullable = True
            self.unique = False
            return
        
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique

    @property
    def d_type(self) -> str:
        return TYPE_BINDINGS\
            .get(self.db_engine, None)\
            .get(self.py_type, None)

    @property
    def constraints(self) -> list[str]:
        mods = []
        if not self.nullable:
            mods.append(SQL_CONSTRAINTS
                        .get(self.db_engine, None)
                        .get("not_null", None))
        if self.primary_key:
            mods.append(SQL_CONSTRAINTS
                        .get(self.db_engine, None)
                        .get("primary_key", None))
        if self.unique:
            mods.append(SQL_CONSTRAINTS
                        .get(self.db_engine, None)
                        .get("unique", None))
        return mods

    def __eq__(self, obj: SQLDataType):
        """Returns True if  obj is equal to self and False if not"""
        return (obj.py_type, obj.nullable, obj.primary_key, obj.unique) == \
            (self.py_type, self.nullable, self.primary_key, self.unique)


class Integer(SQLDataType):
    def __init__(self, nullable: bool = True, primary_key: bool = False, unique: bool = False):
        super().__init__(int, nullable=nullable,
                         primary_key=primary_key, unique=unique)


class Float(SQLDataType):
    def __init__(self, nullable: bool = True, unique: bool = False):
        super().__init__(float, nullable=nullable, unique=unique)


class Text(SQLDataType):
    def __init__(self, nullable: bool = True, unique: bool = False):
        super().__init__(str, nullable=nullable, unique=unique)


class NullType(SQLDataType):
    def __init__(self):
        super().__init__(None)
