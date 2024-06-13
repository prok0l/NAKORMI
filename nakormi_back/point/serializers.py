from rest_framework import serializers

from feed.models import Tag
from point.models import Point
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
    district = serializers.CharField(source='district.name')

    @staticmethod
    def convert_district(validated_data):
        if validated_data.get('district'):
            district = District.objects.filter(name=validated_data.get('district').get('name'))
            if district:
                validated_data['district'] = district[0]
            else:
                raise serializers.ValidationError("District Not Found")

    def create(self, validated_data):
        self.convert_district(validated_data)
        return Point.objects.create(**validated_data)

    def update(self, instance, validated_data):
        self.convert_district(validated_data)
        super().update(instance, validated_data)
        return instance

    class Meta:
        model = Point
        fields = '__all__'
