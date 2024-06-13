from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    name: str
    phone: str
    email: str
    avatar: str
