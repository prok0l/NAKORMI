from rest_framework import serializers

from .models import District, Photo
from user.models import Volunteer


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    photo = serializers.CharField(source='get_photo', read_only=True)
    url = serializers.CharField(source='get_url', read_only=True)
    class Meta:
        model = Photo
        fields = '__all__'
        extra_kwargs = {'id': {'read_only':True}}

    def to_representation(self, instance):
        return instance.pk



class UserField(serializers.RelatedField):
    def to_internal_value(self, data):
        user = Volunteer.objects.filter(tg_id=data)
        if not user:
            raise serializers.ValidationError("User does not exist")
        return user[0]

    def to_representation(self, value):
        return value.tg_id


class TgIdSerializer(serializers.Serializer):
    """Сереализатор получения Volunteer из Tg-Id в headers"""
    tg_id = UserField(queryset=Volunteer.objects.all())

    class Meta:
        fields = ('tg_id', )


