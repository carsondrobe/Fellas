"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from . import views
from django.urls import path
from .views import weather_stations_information
from .views import station_data


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register"),
    path(
        "weather_stations_information/",
        weather_stations_information,
        name="weather_stations_information",
    ),
    path("submit_feedback/", views.submit_feedback, name="submit_feedback"),
    path("weather/", views.weather, name="weather"),
    path("fire/", views.fire, name="fire"),
    path("station_data/", station_data, name="station_data"),
    path(
        "station_data/<str:datetime>/",
        views.station_data,
        name="station_data_with_date",
    ),
    path("view_feedback/", views.view_feedback, name="view_feedback"),
    path(
        "update_feedback_status/",
        views.update_feedback_status,
        name="update_feedback_status",
    ),
    path("add_to_favourites/", views.add_to_favourites, name="add_to_favourites"),
    path("display_fav_button/", views.display_fav_button, name="display_fav_button"),
]
