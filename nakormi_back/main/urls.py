from django.urls import path

from .views import *

app_name = 'main'

urlpatterns = [
    path('districts/', DistrictView.as_view({'get': 'list', 'post': 'create'}, name='districts')),
    path('photo/<int:pk>', PhotoView.as_view({'get':'retrieve'}), name = 'photo'),
    path('photo/upload', UploadPhotoView.as_view({'post':'create'}), name = 'Upload Photo')
]
