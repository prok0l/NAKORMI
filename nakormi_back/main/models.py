from django.db import models
from rest_framework.reverse import reverse


# Create your models here.
class Photo(models.Model):
    photo = models.ImageField(upload_to='images/')

    objects = models.Manager()
    def get_photo(self):
        return self.pk

    def get_url(self):
        return reverse('PhotoView', args = [str(self.pk)])


class Action(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=40)

    def __str__(self):
        return self.name
