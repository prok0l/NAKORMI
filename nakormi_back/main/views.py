from django.shortcuts import render
from rest_framework import mixins, viewsets

from main.models import Photo


# Create your views here.
class PhotoView(mixins.CreateModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
