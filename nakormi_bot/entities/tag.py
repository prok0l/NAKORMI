from dataclasses import dataclass


@dataclass
class Tag:
    id: int
    name: str
    level: int
