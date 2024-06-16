from dataclasses import dataclass


@dataclass
class Point:
    id: int | None
    district: str
    name: str
    address: str
    lat: float
    lon: float
    photo: str | None
    phone: str | None
    info: str | None
    is_active: bool = True
