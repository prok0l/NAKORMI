from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('edit/<int:pk>', VolunteerView.as_view(), name='Create Volunteer'),
    path('inventory/', InventoryView.as_view({'get':'list'}))
]
