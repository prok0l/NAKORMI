from rest_framework import serializers

from .models import District, Photo
from user.models import Volunteer


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    photo_list = serializers.ListField()

    class Meta:
        model = Photo


class UserField(serializers.RelatedField):
    def to_internal_value(self, data):
        user = Volunteer.objects.filter(tg_id=data)
        if not user:
            raise serializers.ValidationError("User does not exist")
        return user[0]


class TgIdSerializer(serializers.Serializer):
    """Сереализатор получения Volunteer из Tg-Id в headers"""
    tg_id = UserField(queryset=Volunteer.objects.all())

    class Meta:
        fields = ('tg_id', )
