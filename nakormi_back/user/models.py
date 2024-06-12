from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator
from django.db import models

from django.core.validators import EMPTY_VALUES
from django.core.exceptions import ValidationError

from feed.models import Tag
from main.models import District


def validate_unique_or_empty_email(value):
    if value not in EMPTY_VALUES and Volunteer.objects.filter(email=value).exists():
        raise ValidationError('This value is not unique.')


def validate_unique_or_empty_phone(value):
    print(value)
    if value not in EMPTY_VALUES and Volunteer.objects.filter(email=value).exists():
        raise ValidationError('This value is not unique.')


class Volunteer(models.Model):
    tg_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True,
                            validators=[
                                RegexValidator(
                                    regex=r'^[А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]*$',
                                    message="Имя не удовлетворяет требованиям"
                                ),
                            ])
    email = models.CharField(max_length=255, blank=True, unique=False, validators=[validate_unique_or_empty_email,
                                                                                   EmailValidator
                                                                                   ])
    phone = models.CharField(max_length=20, blank=True, null=True,
                             validators=[RegexValidator(
                                 regex=r'^\+[\d]+$',
                                 message="Телефон не удовлетворяет требованиям"
                             ),
                                 validate_unique_or_empty_phone
                             ])
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    passport = models.ImageField(upload_to="passport_images/", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_warehouse = models.BooleanField(default=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "volunteers"

    def __str__(self):
        return str(self.tg_id)


class Warehouse(models.Model):
    name = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(Volunteer, on_delete=models.CASCADE, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return str(self.address)


class Inventory(models.Model):
    tg_id = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    volume = models.IntegerField(default=0)
