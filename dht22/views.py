from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.template import Template, Context
from django.utils import timezone
from django.core import serializers
from dht22.models import Sensordata

# Create your views here.
def index(request):
    return render(request, "dht22/chart.html")

# Sends latest humidity and temperature values
def currentview(request):
    sensordata = Sensordata.objects.order_by('-time')[0]
    context = {
        'humidity': sensordata.humidity,
        'temperature': sensordata.temperature,
    }
    
    return JsonResponse({'humidity': sensordata.humidity, 'temperature': sensordata.temperature})

# Gets data from db for given time period, if no time period given show data for last 24h
def dataview(request, time_start=None, time_end=None):
    # No specific time period given -> show last 24h
    if time_end is None:
        time_end = timezone.now()
    if time_start is None:
        time_start = time_end - timezone.timedelta(1)

    # if end is before start, swap them
    if time_end < time_start:
        time_start, time_end = time_end, time_start

    sensordata = Sensordata.objects.order_by('-time').filter(time__range=(time_start, time_end)).values('time', 'humidity', 'temperature')
    
    # no need to return too accurate values for long timeperiods also limits the traffic generated by json
    sensordata = sensordata[::int(len(sensordata)/256+1)]
   
    context = dict()
    context['data'] = sensordata
    return render(request, "dht22/data.json", context)

# Parses given time period and calls dataview with valid parameters
def selectionview(request, sday, smonth, syear, eday, emonth, eyear):
    # try converting input to correct type
    try:
        sday = int(sday)
        smonth = int(smonth)
        syear = int(syear)
        eday = int(eday)
        emonth = int(emonth)
        eyear = int(eyear)

        time_start = timezone.datetime(syear, smonth, sday)
        time_end = timezone.datetime(eyear, emonth, eday)
        time_start = timezone.make_aware(time_start)
        time_end = timezone.make_aware(time_end)
    except:
        raise Http404()
    return dataview(request, time_start, time_end)

