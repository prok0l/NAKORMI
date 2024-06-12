from rest_framework import serializers

from .models import District, Photo


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    photo_list = serializers.ListField()

    class Meta:
        model = Photo
