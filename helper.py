from dataclasses import dataclass
from typing import Generic, TypeVar, Callable

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Option(Generic[T, U]):
    prompt: str
    func: Callable[T, U]


def index(options: dict[str, Option]) -> None:
    for i, option in options.items():
        print(f"{i}. {option.prompt}")


def choice(options: dict[str, Option]) -> Option:
    key = input("Enter an option: ")
    return options.get(key, None)
