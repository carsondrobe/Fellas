from django.shortcuts import render
from django.http import JsonResponse
from .models import WeatherStation

# Create your views here.
def home(request):
    return render(request, "home.html", {})
def weather_stations_data(request):
    stations = WeatherStation.objects.all()
    data = [{
        'latitude': station.Y,
        'longitude': station.X,
        'name': station.STATION_NAME,
        'id': station.WEATHER_STATIONS_ID,
        'elevation': station.ELEVATION,
        'install_date': station.INSTALL_DATE.strftime('%Y-%m-%d')
    } for station in stations]
    return JsonResponse(data, safe=False)