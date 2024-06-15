from django.core.validators import RegexValidator
from rest_framework import serializers

from feed.serializers import TagViewSerializer
from main.serializers import UserField
from point.serializers import ContentField
from .models import Volunteer, Inventory
from main.models import District


class VolunteerSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField(required=False)

    def update(self, instance, validated_data):
        if self.initial_data.get('district'):
            district = District.objects.filter(name=self.initial_data.get('district'))
            if district:
                validated_data['district'] = district[0]
            else:
                raise serializers.ValidationError("District Not Found")
        super().update(instance, validated_data)
        return instance

    @staticmethod
    def get_district(obj):
        if obj.district:
            return obj.district.name
        return None

    class Meta:
        model = Volunteer
        fields = ["name", "email", "phone", "image", "is_active", "is_admin", "district"]


class InventorySerializer(serializers.ModelSerializer):
    tags = TagViewSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ('__all__')


class ShareFeedSerializer(serializers.Serializer):
    content = serializers.ListField(child=ContentField())
    to_user = UserField(queryset=Volunteer.objects.all())


class DistrictField(serializers.RelatedField):
    def to_internal_value(self, data):
        district = District.objects.filter(id=data)
        if not district:
            raise serializers.ValidationError("District does not exist")
        return district[0]


class UsageFeedSerializer(serializers.Serializer):
    content = serializers.ListField(child=ContentField())
    district = DistrictField(queryset=District.objects.all())


class VolunteerReportSerializer(serializers.Serializer):
    summ_take_feed = serializers.IntegerField()
    summ_share_feed = serializers.IntegerField()
    summ_using_feed = serializers.IntegerField()


