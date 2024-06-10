from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('update/<int:pk>', UpdateVolunteer.as_view(), name='Create Volunteer'),
]