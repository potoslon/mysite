from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name = 'home'),
    path('about-us', views.about, name = 'about'),
    path('geolocation', views.geo, name = 'geo'),
]
