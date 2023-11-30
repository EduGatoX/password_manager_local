from enum import Enum
from dataclasses import dataclass


class Messages(Enum):
    SIGN_UP_SUCCESS = "sign_up_success"
    SIGN_UP_FAILURE = "sign_up_failure"
    LOGIN_SUCCESS = "login_success"
    QUIT = "quit"


@dataclass
class Message[T]:
    message: str
    data: T
