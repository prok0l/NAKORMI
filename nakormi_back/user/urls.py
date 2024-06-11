from django.urls import path

from .views import *

app_name = 'user'



urlpatterns = [
    path('edit/<int:pk>', VolunteerView.as_view(), name='Create Volunteer'),
]