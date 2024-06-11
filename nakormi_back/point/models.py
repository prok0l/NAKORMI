from django.db import models


class Point(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    photo = models.ImageField(upload_to="points", blank=True)
    city = models.CharField(max_length=40)
    def __str__(self):
        return self.name
