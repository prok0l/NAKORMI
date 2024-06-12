from rest_framework import serializers

from feed.models import Tag
from point.models import Point
from user.models import Volunteer


class TagField(serializers.RelatedField):
    def to_internal_value(self, data):
        tag = Tag.objects.filter(pk=data)
        if not tag:
            raise serializers.ValidationError("Tag does not exist")
        return tag[0]


class ContentField(serializers.Serializer):
    tags = serializers.ListField(child=TagField(queryset=Tag.objects.all()))
    volume = serializers.IntegerField()


class UserField(serializers.RelatedField):
    def to_internal_value(self, data):
        user = Volunteer.objects.filter(tg_id=data)
        if not user:
            raise serializers.ValidationError("User does not exist")
        return user[0]


class ReceptionSerializer(serializers.Serializer):
    tg_id = UserField(queryset=Volunteer.objects.all())
    content = serializers.ListField(child=ContentField())


class PointSerializer(serializers.ModelSerializer):
    tg_id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Point
        fields = '__all__'

