"""This module contains the relationship between python types and sql types"""

# To add a new engine
# 1. Create a new dictionary with pairs "python_type": "sql_datatype" of the corresponding engine
# 2. Add the relationship in "python_sql_type_relationships" dictionary, using a string as key (that
# string will be used in the configuration)

# sqlite type relationship
python_sqlite_type_relationship = {
    int: "INTEGER",
    float: "REAL",
    str: "TEXT",
    None: "NULL",
}

# sqlite type modifiers
sqlite_type_modifiers = {
    "not_null": "NOT NULL",
    "primary_key": "PRIMARY KEY",
    "unique": "UNIQUE",
}

# Relationship between engines and type relationships
python_sql_type_relationships = {
    "sqlite3": python_sqlite_type_relationship,
}

# Relationship between engines and type modifiers
engine_sql_type_modifiers_relationships = {
    "sqlite3": sqlite_type_modifiers,
}


class SQLDataType:
    def __init__(self, db_engine: str, py_type: type, nullable: bool = True,
                 primary_key: bool = False, unique: bool = False):
        self.db_engine = db_engine
        self.py_type = py_type
        self.nullable = nullable if not primary_key else False
        self.primary_key = primary_key
        self.unique = unique

    @property
    def d_type(self) -> str:
        return python_sql_type_relationships\
            .get(self.db_engine, None)\
            .get(self.py_type, None)

    @property
    def modifiers(self) -> list[str]:
        mods = []
        if not self.nullable:
            mods.append(engine_sql_type_modifiers_relationships
                        .get(self.db_engine, None)
                        .get("not_null", None))
        if self.primary_key:
            mods.append(engine_sql_type_modifiers_relationships
                        .get(self.db_engine, None)
                        .get("primary_key", None))
        if self.unique:
            mods.append(engine_sql_type_modifiers_relationships
                        .get(self.db_engine, None)
                        .get("unique", None))
        return mods

    def __repr__(self) -> str:
        return str(self.__class__)


class Integer(SQLDataType):
    def __init__(self, db_engine: str, nullable: bool = True, primary_key: bool = False, unique: bool = False):
        super().__init__(db_engine, int, nullable=nullable,
                         primary_key=primary_key, unique=unique)


class Float(SQLDataType):
    def __init__(self, db_engine: str, nullable: bool = True, unique: bool = False):
        super().__init__(db_engine, float, nullable=nullable, unique=unique)


class Text(SQLDataType):
    def __init__(self, db_engine: str, nullable: bool = True, unique: bool = False):
        super().__init__(db_engine, str, nullable=nullable, unique=unique)


class NullType(SQLDataType):
    def __init__(self, db_engine: str):
        super().__init__(db_engine, None)
