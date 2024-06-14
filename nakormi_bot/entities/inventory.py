from dataclasses import dataclass
from typing import List


@dataclass
class InventoryLine:
    id: int
    tags: List[str]
    volume: int
    tg_id: int
