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

# Relationship between engines and type relationships
python_sql_type_relationships = {
    "sqlite3": python_sqlite_type_relationship,
}


class SQLDataType[T]:
    def __init__(self, db_engine: str, py_type: type, value: T, nullable: bool = True, primary_key: bool = False):
        self.db_engine = db_engine
        self.py_type = py_type
        self.value = value
        self.nullable = nullable if not primary_key else False
        self.primary_key = primary_key

    @property
    def sql_type(self) -> str:
        sql = python_sql_type_relationships.get(self.db_engine, None).get(self.py_type, None)
        sql += "" if self.nullable else " NOT NULLABLE"     # TODO: Should be dependent on db_engine and now it's hard coded
        sql += "" if not self.primary_key else " PRIMARY KEY" # TODO: Should be dependent on db_engine and now it's hard coded
        return sql
    
    def __str__(self) -> str:
        return str(self.value)


class Integer(SQLDataType[int]):
    def __init__(self, db_engine: str, value: int, nullable: bool = True, primary_key: bool = False):
        super().__init__(db_engine, int, value, nullable=nullable, primary_key=primary_key)


class Float(SQLDataType[float]):
    def __init__(self, db_engine: str, value: float, nullable: bool = True):
        super().__init__(db_engine, float, value, nullable=nullable)


class Text(SQLDataType[str]):
    def __init__(self, db_engine: str, value: str, nullable: bool = True):
        super().__init__(db_engine, str, value, nullable=nullable)


class NullType(SQLDataType[None]):
    def __init__(self, db_engine: str):
        super().__init__(db_engine, None, None)
