from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    name: str
    phone: str
    email: str
    image: str | None
    is_active: bool = False
    is_admin: bool = False
    district: str | None = None
