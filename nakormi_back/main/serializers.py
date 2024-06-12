from rest_framework import  serializers

from main.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    photo_list = serializers.ListField()
    class Meta:
        model = Photo
