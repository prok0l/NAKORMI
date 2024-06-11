from django.urls import path

from .views import *

app_name = 'feed'

urlpatterns = [
    path('tags/<int:level>', GetTags.as_view(), name='Create Volunteer'),
]
