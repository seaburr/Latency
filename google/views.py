from django.shortcuts import render
from django.utils import timezone
from .models import LoadTimes, TestSites
import requests
import datetime
import pygal
from pygal.style import DarkStyle


# Create your views here.
def index(request):
    page_load_ts = datetime.datetime.now(tz=timezone.utc)
    urls = []
    for url in TestSites.objects.all():
        new_load_entry(url, page_load_ts)
        urls.append(url.url)

    load_chart = LoadChart(
        chart_name='Page Load Times (in ms)',
        urls=urls,
        height=900,
        width=1600,
        explicit_size=True,
        style=DarkStyle,
        x_label_rotation=20
    ).generate()

    return render(request, 'base.html', {'page_title': 'Load Times', 'cht': load_chart})



def new_load_entry(TestSite, timestamp):
    response = requests.get(TestSite.url)
    loadtime_in_ms = response.elapsed.microseconds / 1000
    LoadTimes(url_id=TestSite, latency=loadtime_in_ms, timestamp=timestamp).save()


class LoadChart(object):
    def __init__(self, chart_name, urls, **kwargs):
        self.chart = pygal.Line(**kwargs)
        self.chart.title = chart_name
        self.urls = urls

    def get_data(self, index):
        data = {}
        # Get the last 20 load times, then reverse.
        for loadtime in LoadTimes.objects.all().filter(url_id=index).order_by('-id')[:20][::-1]:
            data[loadtime.timestamp] = loadtime.latency
        return data

    def generate(self):
        for url in self.urls:
            data = self.get_data(self.urls.index(url))

            timestamps = []
            latency = []
            for key, value in data.items():
                timestamps.append(key)
                latency.append(value)

            self.chart.x_labels = map(str, timestamps)
            self.chart.add(url, latency)

        return self.chart.render(is_unicode=True)

