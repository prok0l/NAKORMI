from rest_framework import serializers

from feed.models import Tag
from point.models import Point
from user.models import Volunteer
from main.models import District


class TagField(serializers.RelatedField):
    def to_internal_value(self, data):
        tag = Tag.objects.filter(pk=data)
        if not tag:
            raise serializers.ValidationError("Tag does not exist")
        return tag[0]


class ContentField(serializers.Serializer):
    tags = serializers.ListField(child=TagField(queryset=Tag.objects.all()))
    volume = serializers.IntegerField()


class ReceptionSerializer(serializers.Serializer):
    content = serializers.ListField(child=ContentField())


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = '__all__'

