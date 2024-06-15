from django.db import models
from django.core.validators import RegexValidator

from main.models import District


class Point(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    lat = models.FloatField()
    is_active = models.BooleanField(default=True)
    lon = models.FloatField()
    photo = models.ImageField(upload_to="points", blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True,
                             validators=[RegexValidator(
                                 regex=r'^\+[\d]+$',
                                 message="Телефон не удовлетворяет требованиям"
                             ),
                             ])
    info = models.CharField(max_length=255, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
