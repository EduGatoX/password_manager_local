from dataclasses import dataclass
from typing import Generic, TypeVar, Callable

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Option(Generic[T, U]):
    prompt: str
    func: Callable[T, U]


def index(options: list[Option]) -> None:
    for i, option in enumerate(options):
        print(f"{i+1}. {option.prompt}")


def choice(options: list[Option]) -> Option|None:
    index = input("Enter an option: ")
    if not 0<=int(index)-1<len(index):
        return None
    return options[int(index)-1]
