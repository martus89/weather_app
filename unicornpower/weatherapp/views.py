import json
import requests
import pandas
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
from .forms import SearchingForm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename="filefile.log")
logger = logging.getLogger(__name__)


def search_view(request):

    form = SearchingForm()

    if request.method == 'POST':
        form = SearchingForm(request.POST)
        if form.is_valid():
            city_input = form.cleaned_data['city_input']
            request.session["city_input"] = city_input
            logger.info(f"{city_input} was requested")
            return redirect("%s?city_input=%s"%(reverse("city_view"), city_input))

    context = {
        'form': form,
        }

    return render(request, 'weatherapp/search_page.html', context)


def city_view(request):
    city = request.GET.get("city_input")
    api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}'
    response_raw = requests.get(api_url, headers={'X-Api-Key': 'yG/ylPn2r4KMn9UgfkTeyw==Bx52sV7iKYlf8ata'})
    if not json.loads(response_raw.text):
        raise Http404
    city_name = json.loads(response_raw.text)[0]['name']
    city_country = json.loads(response_raw.text)[0]['country']
    city_lat = json.loads(response_raw.text)[0]['latitude']
    city_long = json.loads(response_raw.text)[0]['longitude']

    response_weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={city_lat}&longitude={city_long}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m')
    my_hours = json.loads(response_weather.text)['hourly']['time']
    my_temp = json.loads(response_weather.text)['hourly']['temperature_2m']

    zipped_data = list(zip(my_hours, my_temp))

    fields = ["Hours", "Temperature"]

    data_read = pandas.DataFrame(zipped_data, columns=fields)

    data_read["Hours"] = pandas.to_datetime(data_read["Hours"])
    data_read["Temperature"] = pandas.to_numeric(data_read["Temperature"])

    graph = figure(title="Upcoming temperatures", width=1000, height=500, x_axis_label='Hours', y_axis_label='Temperature')

    graph.xaxis[0].formatter = DatetimeTickFormatter(days=["%d %b, %Y"])

    graph.line(data_read["Hours"], data_read["Temperature"], legend_label="Temp", line_width=2)
    script, div = components(graph)

    context = {
        "city_name": city_name,
        "city_country": city_country,
        "script": script,
        "div": div,
        "zipped_data": zipped_data,
    }

    return render(request, 'weatherapp/forecast_page.html', context)
