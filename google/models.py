from django.db import models


class LoadTimes(models.Model):
    url = models.CharField(max_length=128)
    latency = models.IntegerField()
    timestamp = models.DateTimeField('latency timestamp')

