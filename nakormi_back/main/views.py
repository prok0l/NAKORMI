from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from .models import District, Photo
from .serializers import DistrictSerializer, PhotoSerializer, PhotoUploadSerializer
from .permissions import IsAdminOrReadOnly

from rest_framework import mixins, viewsets


# Create your views here.
class PhotoView( mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Загрузка фотографии"""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class DistrictView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """Просмотр, создание, редактирование округов"""
    permission_classes = [HasAPIKey, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']
    serializer_class = DistrictSerializer
    queryset = District.objects.all()




class UploadPhotoView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = PhotoUploadSerializer
    queryset = Photo.objects.all()
    def create(self, request, *args, **kwargs):
        uploaded_files = self.request.FILES.getlist('photo')
        photo_list = []
        for file in uploaded_files:
            photo = Photo.objects.create(photo=file)
            photo.save()
            photo_list.append(photo)
        return Response([x.pk for x in photo_list], status=status.HTTP_201_CREATED)