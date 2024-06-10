from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class Volunteer(models.Model):
    tg_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True,
                            validators=[
                                RegexValidator(
                                    regex=r'^[А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]*$',
                                    message="Имя не удовлетворяет требованиям"
                                ),
                            ])
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True,
                             validators=[RegexValidator(
                                 regex=r'^\+[\d]+$',
                                 message="Телефон не удовлетворяет требованиям"
                             )],
                             unique=True)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    passport = models.ImageField(upload_to="passport_images/", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "volunteers"

    def __str__(self):
        return str(self.tg_id)