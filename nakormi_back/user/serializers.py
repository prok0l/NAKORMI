from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Volunteer
from main.models import District


class VolunteerSerializer(serializers.ModelSerializer):
    district = serializers.CharField(source='district.name')

    def update(self, instance, validated_data):
        if validated_data.get('district'):
            district = District.objects.filter(name=validated_data.get('district').get('name'))
            if district:
                validated_data['district'] = district[0]
            else:
                raise serializers.ValidationError("District Not Found")
        super().update(instance, validated_data)
        return instance

    class Meta:
        model = Volunteer
        fields = ["name", "email", "phone", "image", "is_active", "is_admin", "district"]

