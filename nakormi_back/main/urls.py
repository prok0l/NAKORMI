from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('districts/', DistrictView.as_view({'get': 'list', 'post': 'create'}, name='districts')),
]
