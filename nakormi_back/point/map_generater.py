from folium import Map, Marker, Icon
from typing import Set
from .models import Point
from user.models import Warehouse
from django.conf import settings

import os


class MapGeneration:
    def __init__(self, points: Set[Point], warehouses: Set[Warehouse]):
        self.points = list(points)
        self.warehouses = list(warehouses)

    @property
    def map(self):
        center = (55.751025, 37.619550)
        if self.points:
            center = (sum(x.lat for x in self.points) / len(self.points),
                      sum(x.lon for x in self.points) / len(self.points))
        elif self.warehouses:
            center = (sum(x.lat for x in self.warehouses) / len(self.warehouses),
                      sum(x.lon for x in self.warehouses) / len(self.warehouses))
        m = Map(location=center, zoom_start=10)
        for point in self.points:
            Marker(
                location=[point.lat, point.lon],
                tooltip=point.name,
                popup=point.address,
                radius=10,
                icon=Icon(color="black",
                          icon_color='white',
                          icon='box-open',
                          prefix='fa'
                          )
            ).add_to(m)
        for warehouse in self.warehouses:
            Marker(
                location=[warehouse.lat, warehouse.lon],
                tooltip=warehouse.name,
                popup=warehouse.address,
                radius=10,
                icon=Icon(color="red",
                          icon_color='white',
                          icon='home'
                          )
            ).add_to(m)

        m.save(os.path.dirname(settings.BASE_DIR) + r'\nakormi_back\point\templates\map.html')
        return 'map.html'
