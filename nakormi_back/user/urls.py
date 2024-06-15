from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('edit/<int:pk>', VolunteerView.as_view(), name='Create Volunteer'),
    path('inventory/', InventoryView.as_view({'get':'list'})),
    path('check/<int:pk>', CheckUserView.as_view(), name='Check'),
    path('share_feed/', ShareFeed.as_view(), name='ShareFeed'),
    path('usage_feed/', UsageFeedView.as_view(), name='ShareFeed'),
]
