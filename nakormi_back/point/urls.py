from django.urls import path

from .views import *

app_name = 'point'

urlpatterns = [
    path('take/<int:point>', TakeFeeds.as_view(), name='Take feeds'),
    path('points/', PointView.as_view({'get': 'list', 'post': 'create'})),
    path('points/<int:pk>',
         PointView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'})),

    path('map/', get_map, name='map'),
]
