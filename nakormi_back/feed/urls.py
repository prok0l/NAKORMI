from django.urls import path

from .views import *

app_name = 'feed'

urlpatterns = [
    path('tags/<int:level>', GetTags.as_view(), name='Create Tags'),
    path('reports/', ReportView.as_view({'get':'list'})),
    path('reports/<int:pk>', ReportView.as_view({'get':'retrieve'})),
    path('transfer/', TransferView.as_view({'get':'list'})),
    path('transfer/<int:pk>', TransferView.as_view({'get':'retrieve'})),
    path('reports/photo', ReportPhotoView.as_view({'post':'create'})),
    path('reports/photo/<int:report>', ReportPhotoView.as_view({'get':'retrieve'}))
]
