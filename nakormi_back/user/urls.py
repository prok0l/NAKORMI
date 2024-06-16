from django.urls import path

from .views import *

app_name = 'user'

urlpatterns = [
    path('edit/<int:pk>', VolunteerView.as_view(), name='Create Volunteer'),
    path('inventory/', InventoryView.as_view({'get':'list'})),
    path('check/<int:pk>', CheckUserView.as_view(), name='Check'),
    path('share_feed/', ShareFeed.as_view(), name='ShareFeed'),
    path('usage_feed/', UsageFeedView.as_view(), name='ShareFeed'),
    path('inventory/analytics/', InventoryAnalytics.as_view({'get': 'list'}), name='InventoryAnalytics'),
    path('volunteer/reports/', VolunteerReportView.as_view()),
    path('add_volunteer/', AddVolunteer.as_view(), name='Add Volunteer'),
]
