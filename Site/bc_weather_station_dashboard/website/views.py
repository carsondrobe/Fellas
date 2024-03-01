from django.shortcuts import render
from django.http import JsonResponse
from .models import WeatherStation

# Create your views here.
def home(request):
    return render(request, "home.html", {})
def weather_stations_data(request):
    stations = WeatherStation.objects.all()
    data = [{
        'id': station.WEATHER_STATIONS_ID,
        'code': station.STATION_CODE,
        'name': station.STATION_NAME,
        'acronym': station.STATION_ACRONYM,
        'latitude': station.Y,
        'longitude': station.X,
        'elevation': station.ELEVATION,
        'install_date': station.INSTALL_DATE.strftime('%Y-%m-%d')
    } for station in stations]
    return JsonResponse(data, safe=False)