from django.urls import path

from .views import *

app_name = 'point'



urlpatterns = [
    path('take/<int:point>', TakeFeeds.as_view(), name='Take feeds'),
]