from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework_api_key.permissions import HasAPIKey

from .models import District, Photo
from .serializers import DistrictSerializer, PhotoSerializer
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




