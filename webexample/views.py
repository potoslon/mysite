from django.shortcuts import render
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from routingpy import MapboxValhalla, Graphhopper
from pprint import pprint
from geopy import distance
import folium
import requests
import json
import overpy

def index(request):

    url = "https://freegeoip.app/json/"

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }

    response = requests.request("GET", url, headers=headers)
    j = json.loads(response.text)
    lat = j['latitude']
    lon = j['longitude']


    m = folium.Map(height=650, location=(lat, lon), zoom_start=10)

    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent="webexample")

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        location_ = form.cleaned_data.get('location')
        location = geolocator.geocode(location_)
        shops = form.cleaned_data.get('shops')
        cafes = form.cleaned_data.get('cafes')
        bars = form.cleaned_data.get('bars')
        fast_food = form.cleaned_data.get('fast_food')
        pharmacy = form.cleaned_data.get('pharmacy')
        fountain = form.cleaned_data.get('fountain')
        bicycle_rental = form.cleaned_data.get('bicycle_rental')
        ice_cream = form.cleaned_data.get('ice_cream')
        supermamrket = form.cleaned_data.get('supermamrket')
        clock = form.cleaned_data.get('clock')
        bureau_de_change = form.cleaned_data.get('bureau_de_change')
        historic = form.cleaned_data.get('historic')
        clothes = form.cleaned_data.get('clothes')
        bakery = form.cleaned_data.get('bakery')
        beauty = form.cleaned_data.get('beauty')
        kiosk = form.cleaned_data.get('kiosk')
        florist = form.cleaned_data.get('florist')

        locationPoint = location.latitude, location.longitude

        destinationPoint = destination.latitude, destination.longitude

        locationMarker = folium.Marker(location=locationPoint, icon=folium.Icon(color='blue')).add_to(m)
        destinationMarker = folium.Marker(location=destinationPoint, icon=folium.Icon(color='red')).add_to(m)

        s = distance.distance(locationPoint, destinationPoint).m
        r = str(s / 2)

        middlelat = str((location.latitude + destination.latitude) / 2)
        middlelon = str((location.longitude + destination.longitude) / 2)
        middlePoint = (middlelat , middlelon)

        middleMarker = folium.Marker(location=middlePoint, icon=folium.Icon(color='black')).add_to(m)

        shopsbool = 0
        amenitybool = 0
        historicbool = 0

        amenity = ""
        if cafes + bars + bureau_de_change + clock + ice_cream + bicycle_rental + fountain + pharmacy + fast_food > 0:

            amenitybool = 1

            if bars == True:
                if amenity == "":
                    amenity += '"bar'
                else:
                    amenity += '|bar'

            if cafes == True:
                if amenity == "":
                    amenity += '"cafe'
                else:
                    amenity += '|cafe'

            if fast_food == True:
                if amenity == "":
                    amenity += '"fast_food'
                else:
                    amenity += '|fast_food'

            if pharmacy == True:
                if amenity == "":
                    amenity += '"pharmacy'
                else:
                    amenity += '|pharmacy'

            if fountain == True:
                if amenity == "":
                    amenity += '"fountain'
                else:
                    amenity += '|fountain'

            if bicycle_rental == True:
                if amenity == "":
                    amenity += '"bicycle_rental'
                else:
                    amenity += '|bicycle_rental'

            if ice_cream == True:
                if amenity == "":
                    amenity += '"ice_cream'
                else:
                    amenity += '|ice_cream'

            if clock == True:
                if amenity == "":
                    amenity += '"clock'
                else:
                    amenity += '|clock'

            if bureau_de_change == True:
                if amenity == "":
                    amenity += '"bureau_de_change'
                else:
                    amenity += '|bureau_de_change'

            amenity = '["amenity"~' + amenity + '"]'
            amenity = '''node(around:'''+r+''','''+middlelat+''','''+middlelon+''')'''+amenity+''';'''


        historic = ""
        if historic == True:
            historicbool = 1
            historic = '["historic"]'
            historic = '''node(around:'''+r+''','''+middlelat+''','''+middlelon+''')'''+historic+''';'''


        shops = ""
        if supermamrket + clothes + bakery + kiosk + florist > 0:
            shopsbool = 1
            if supermamrket == True:
                if shops == "":
                    shops += '"supermarket'
                else:
                    shops += '|supermarket'

            if clothes == True:
                if shops == "":
                    shops += '"clothes'
                else:
                    shops += '|clothes'

            if bakery == True:
                if shops == "":
                    shops += '"bakery'
                else:
                    shops += '|bakery'

            if beauty == True:
                if shops == "":
                    shops += '"beauty'
                else:
                    shops += '|beauty'

            if kiosk == True:
                if shops == "":
                    shops += '"kiosk'
                else:
                    shops += '|kiosk'

            if florist == True:
                if shops == "":
                    shops += '"florist'
                else:
                    shops += '|florist'

            shops = '["shop"~' + shops + '"]'
            shops = '''node(around:'''+r+''','''+middlelat+''','''+middlelon+''')'''+shops+''';'''


        locationPoint = location.latitude, location.longitude

        destinationPoint = destination.latitude, destination.longitude

        locationMarker = folium.Marker(location=locationPoint, icon=folium.Icon(color='blue'), popup=location.address).add_to(m)
        destinationMarker = folium.Marker(location=destinationPoint, icon=folium.Icon(color='red'), popup=destination.address).add_to(m)

        s = distance.distance(locationPoint, destinationPoint).m
        r = str(s / 2)

        middlelat = str((location.latitude + destination.latitude) / 2)
        middlelon = str((location.longitude + destination.longitude) / 2)
        middlePoint = (middlelat , middlelon)

        middleMarker = folium.Marker(location=middlePoint, icon=folium.Icon(color='black')).add_to(m)

        if shopsbool + amenitybool + historicbool > 1 :
            api = overpy.Overpass()
            result = api.query('''
            [out:json];
            (
            '''+amenity+'''
            '''+historic+'''
            '''+shops+'''
            ) -> .a;
            .a out;
            ''')
        else :
            api = overpy.Overpass()
            result = api.query('''
            [out:json];
            '''+amenity+'''
            '''+historic+'''
            '''+shops+'''
            out body;
            ''')

        nodeArray = [[location.longitude, location.latitude]]
        i = 0
        print(len(result.nodes))
        for node in result.nodes:
            print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
            nodeArray = nodeArray + [[float(node.lon), float(node.lat)]]
            i = i + 1

        if i > 0:
            if i < 24:
                nodeArray = nodeArray + [[destination.longitude, destination.latitude]]
                coords = nodeArray[:]
            else:
                nodeArray[24] = destination.longitude, destination.latitude
                coords = nodeArray[0:25]
                i = 23


            client = MapboxValhalla(api_key='pk.eyJ1IjoicG90b3Nsb24iLCJhIjoiY2toZ2RjanU0MGgzczJ5cXFjcm51Z253cSJ9.10HE4dkyAnWm8fajZIfecw')
            matrix = client.matrix(locations=coords, profile='pedestrian')

            pprint((matrix.distances))


            distances = matrix.distances
            Points = i+1
            c = 0
            i = 0
            Num_of_POI = 0
            Found_POI_num = 0
            res = []
            dop = []
            dist = distances[0][Points]
            range = 2 * distances[0][Points]
            while dist < range and Num_of_POI < 3:
                k = 1000000
                Num_of_POI+=1
                j = 0
                while j < Points:
                    s = 0
                    Flag = 0
                    while s < Found_POI_num:
                        if j == res[s]:
                            Flag = 1
                        s+=1

                    if i != j and Flag == 0:
                        c = distances[i][j] + distances[Points][j]
                        if c < k:
                            k = c
                            g = j
                    j+=1
                dop = dop + [distances[0][i]]
                res = res + [i]
                dist = dist + distances[i][g] + distances[g][Points] - distances[i][Points]
                Found_POI_num+=1
                i = g
            res+=[Points]
            dop += [distances[0][Points]]

            j = 0
            while j < Found_POI_num - 1:
                i = j
                while dop[i] > dop[i+1]:
                    t = dop[i]
                    n = res[i]
                    res[i] = res[i+1]
                    res[i+1] = n
                    dop[i] = dop[i+1]
                    dop[i+1] = t
                    i+=1
                j+=1

            print(res)

            POI = []

            for o in res:
                POI = POI + [coords[o]]
                POIMarker = folium.Marker(location=(coords[o][1], coords[o][0]), icon=folium.Icon(color='green')).add_to(m)
            print(POI)

            client = MapboxValhalla(api_key='pk.eyJ1IjoicG90b3Nsb24iLCJhIjoiY2toZ2RjanU0MGgzczJ5cXFjcm51Z253cSJ9.10HE4dkyAnWm8fajZIfecw')
            route = client.directions(locations=POI, profile='pedestrian')

            pprint((route.geometry, route.duration, route.distance, route.raw))

            a = len(route.geometry) - 1
            q = 0
            while q < a:
                line = folium.PolyLine(locations=[[route.geometry[q][1],route.geometry[q][0]],[route.geometry[q+1][1],route.geometry[q+1][0]]],
                 weight=5, color='blue')
                m.add_child(line)
                q+=1


    m = m._repr_html_()

    context = {
    'form' : form,
    'map' : m,
    }


    return render(request, 'webexample/index.html', context)


def about(request):
    return render(request, 'webexample/about.html')



def geo(request):
    return render(request, 'webexample/geo.html')


from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
