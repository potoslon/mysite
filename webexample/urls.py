from django.urls import path, include
from . import views
from .views import SignUpView


urlpatterns = [
    path('', views.index, name = 'home'),
    path('about-us', views.about, name = 'about'),
    path('geolocation', views.geo, name = 'geo'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
