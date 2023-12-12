from dataclasses import dataclass
from typing import Callable


@dataclass
class Option[T, U]:
    prompt: str
    func: Callable[[T], U]


def index(options: list[Option]) -> None:
    for i, option in enumerate(options):
        print(f"{i+1}. {option.prompt}")


def choice(options: list[Option]) -> Option | None:
    index = input("Enter an option: ")
    # handle invalid inputs
    if not index.isdigit():
        return None
    if not (0 <= int(index) - 1 < len(options)):
        return None
    return options[int(index) - 1]
