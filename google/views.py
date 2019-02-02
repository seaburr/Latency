from django.shortcuts import render
from django.utils import timezone
from .models import LoadTimes
import requests
import datetime
import pygal
from pygal.style import DarkStyle


# Create your views here.
def index(request):
    new_load_entry('https://google.com')

    load_chart = LoadChart(
        chart_name='Page Load Times (in ms)',
        url='https://google.com',
        height=900,
        width=1600,
        explicit_size=True,
        style=DarkStyle,
        x_label_rotation=20
    ).generate()

    return render(request, 'base.html', {'page_title': 'Load Times', 'cht': load_chart})



def new_load_entry(url):
    response = requests.get(url)
    loadtime_in_ms = response.elapsed.microseconds / 1000
    LoadTimes(url=url, latency=loadtime_in_ms, timestamp=datetime.datetime.now(tz=timezone.utc)).save()


class LoadChart(object):
    def __init__(self, chart_name, url, **kwargs):
        self.chart = pygal.Line(**kwargs)
        self.chart.title = chart_name
        self.url = url

    def get_data(self):
        data = {}
        # Get the last 20 load times, then reverse.
        for loadtime in LoadTimes.objects.all().order_by('-id')[:20][::-1]:
            data[loadtime.timestamp] = loadtime.latency
        return data

    def generate(self):
        data = self.get_data()

        timestamps = []
        latency = []
        for key, value in data.items():
            timestamps.append(key)
            latency.append(value)

        self.chart.x_labels = map(str, timestamps)
        self.chart.add(self.url, latency)

        return self.chart.render(is_unicode=True)

