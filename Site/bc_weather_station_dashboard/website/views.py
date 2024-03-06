from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

from .forms import FeedbackForm
from django.http import JsonResponse
from .models import WeatherStation


def home(request):
    return render(request, "home.html", {})
  
def fire(request):
    return render(request, "fire.html", {})
  
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return HttpResponse('Please fill in all fields', status=400)
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is valid, log them in
            login(request, user)
            # Redirect to the home page
            return redirect(reverse('home'))
        else:
            # Invalid username or password
            return HttpResponse('Invalid username or password', status=400)
    
    return render(request, 'login.html')

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
            # TODO: Save the feedback to the database
            # For right now just prints the feedback to the console
            print(form.cleaned_data["feedback"])
            return redirect("home")
    else:
        form = FeedbackForm()
    return redirect("home")
