from typing import Any
from .typing import SQLDataType


class Table(type):
    """Metaclass that represents a Table. The main objectives of this metaclass are:

    1) Filter the class attributes so that it guarantees that they are an instance
    of SQLDataType (see ./models/typing.py)

    2) Create new properties based on the class attributes that are generalized across
    all tables.
    """
    __tablename__ = None

    def __new__(cls, name, bases, attrs: dict[str, Any]):
        # Filter the attributes to those created by the user
        filtered_dict = dict(filter(lambda item: not item[0].startswith("__"),
                                    attrs.items()))

        # Check that all attributes created by the user are of type SQLDataType
        for key, value in filtered_dict.items():
            if not isinstance(value, SQLDataType):
                raise TypeError(f"{key} must be of type SQLDataType."
                                + f"Failed with {key=}, {value=}.")

        return super().__new__(cls, name, bases, attrs)

    @property
    def __schema__(cls) -> dict[str, SQLDataType]:
        """Returns the schema of this table as a dictionary where:

        1) The keys are the columns names of the table.

        2) The values are elements of type SQLDataType that represent the data type
        and its sql modifiers (e.g. PRIMARY KEY, NOT NULL, UNIQUE, etc...)"""

        # Filter the attributes to those created by the user
        filtered_dict = dict(filter(lambda item: not item[0].startswith("__"),
                                    cls.__dict__.items()))

        return filtered_dict


class TableModel(metaclass=Table):
    pass
