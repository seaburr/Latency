from django.db import models


class TestSites(models.Model):
    url = models.CharField(max_length=128)

    def __str__(self):
        return self.url


class LoadTimes(models.Model):
    url_id = models.ForeignKey(TestSites, on_delete=models.CASCADE)
    latency = models.IntegerField()
    timestamp = models.DateTimeField('latency timestamp')

    def __str__(self):
        return self.latency
