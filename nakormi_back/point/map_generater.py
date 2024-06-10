from folium import Map, Marker
from typing import Set
from .models import Point
from django.conf import settings

import os


class MapGeneration:
    def __init__(self, points: Set[Point]):
        self.points = points

    @property
    def map(self):
        m = Map(location=(55.751025, 37.619550))
        for point in self.points:
            Marker(
                location=[point.lat, point.lon],
                tooltip=point.name,
                popup=point.address,
            ).add_to(m)

        m.save(os.path.dirname(settings.BASE_DIR) + r'\nakormi_back\point\templates\map.html')
        return 'map.html'
