from dataclasses import dataclass


@dataclass
class Point:
    id: int
    district: str
    name: str
    address: str
    lat: float
    lon: float
    photo: str | None
    phone: str | None
    info: str | None
