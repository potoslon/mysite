from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
import folium
import requests
import json



def index(request):
    m = folium.Map(height=650, location=(54.715424, 20.509207), zoom_start=12)


    url = "https://freegeoip.app/json/"

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }

    response = requests.request("GET", url, headers=headers)
    j = json.loads(response.text)
    lat = j['latitude']
    lon = j['longitude']


    location = folium.Marker(location=[lat, lon], icon=folium.Icon(color='blue')).add_to(m)

    destination = folium.ClickForMarker().add_to(m)


    m = m._repr_html_()


    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)

    context = {
    'form' : form,
    'distance' : obj,
    'map' : m
    }



    return render(request, 'webexample/index.html', context) #{'title': 'Main page', 'tasks': tasks})


def about(request):
    return render(request, 'webexample/about.html')



def geo(request):
    return render(request, 'webexample/geo.html')
