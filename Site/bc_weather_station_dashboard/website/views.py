from django.shortcuts import render, redirect

from .forms import FeedbackForm
from django.http import JsonResponse
from .models import WeatherStation, Feedback
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    return render(request, "home.html", {})


def weather_stations_data(request):
    stations = WeatherStation.objects.all()
    data = [
        {
            "id": station.WEATHER_STATIONS_ID,
            "code": station.STATION_CODE,
            "name": station.STATION_NAME,
            "acronym": station.STATION_ACRONYM,
            "latitude": station.Y,
            "longitude": station.X,
            "elevation": station.ELEVATION,
            "install_date": station.INSTALL_DATE.strftime("%Y-%m-%d"),
        }
        for station in stations
    ]
    return JsonResponse(data, safe=False)


def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                message=form.cleaned_data["feedback"],
                user=request.user,
                status=Feedback.SUBMITTED,
            )
            feedback.save()

            return redirect("home")

    return redirect("home")
