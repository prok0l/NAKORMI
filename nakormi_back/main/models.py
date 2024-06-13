from django.db import models


# Create your models here.
class Photo(models.Model):
    photo = models.ImageField(upload_to='images/')


class Action(models.Model):
    name = models.CharField(max_length=70)


class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=40)

    def __str__(self):
        return self.name
