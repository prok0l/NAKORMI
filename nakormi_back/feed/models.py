import datetime

from django.db import models

from main.models import Photo, Action

from user.models import Tag


# Create your models here.


class Report(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)
    from_user = models.ForeignKey('user.Volunteer', on_delete=models.PROTECT, related_name='from_user', blank=True,
                                  null=True)
    to_user = models.ForeignKey('user.Volunteer', on_delete=models.PROTECT, related_name='to_user', blank=True,
                                null=True)
    point = models.ForeignKey('point.Point', blank=True, on_delete=models.PROTECT, null=True)


class Transfer(models.Model):
    report = models.ForeignKey(Report, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    volume = models.IntegerField()


class ReportPhoto(models.Model):
    photo = models.ManyToManyField(Photo)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)


class TransferPhoto(models.Model):
    photo = models.ManyToManyField(Photo)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
