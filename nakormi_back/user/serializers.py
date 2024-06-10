from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Volunteer


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ["tg_id", "name", "email", "phone", "is_active"]
