from entities.point import Point
from functional.phrases import Phrases

from typing import List


def represent_points(points: List[Point], phrase: Phrases) -> str:
    string = ""
    for ind, item in enumerate(points):
        string += phrase['point']['points_item'].format(ind=ind + 1, district=item.district,
                                                        name=item.name, address=item.address)
    return string

