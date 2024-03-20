from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import FeedbackForm
from django.http import JsonResponse
from .models import WeatherStation, Feedback, StationData
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

current_page = "weather"


def home(request, **kwargs):
    if current_page == "weather":
        return weather(request, **kwargs)
    elif current_page == "fire":
        return fire(request, **kwargs)
    else:
        raise ValueError("Invalid page", current_page)


def weather(request, **kwargs):
    global current_page
    current_page = "weather"
    return render(request, "weather.html", kwargs)


def fire(request, **kwargs):
    global current_page
    current_page = "fire"
    return render(request, "fire.html", kwargs)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            return HttpResponse("Please fill in all fields", status=400)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is valid, log them in
            login(request, user)
            # Redirect to the home page
            return redirect(reverse("home"))
        else:
            # Invalid username or password
            return home(request, error="Invalid username or password")

    return home(request, error="Invalid request")


def logout_user(request):
    logout(request)
    return home(request)


def register(request):
    print("register", request.POST)
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    if not username or not email or not password:
        return HttpResponse("Please fill in all fields", status=400)

    # Create the user
    user = User.objects.create_user(username, email, password)
    user.save()
    # Log the user in
    login(request, user)

    return redirect(reverse("home"))


def weather_stations_information(request):
    # Get all stations
    stations = WeatherStation.objects.all()
    # Check if stations is empty
    if not stations.exists():
        # Return an empty JSON response of an error message indicating no data was found
        return JsonResponse(
            {"error": "No data found for the specified date and time"}, status=404
        )
    # Create dictionary of data
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
    # Return the data as a json response
    return JsonResponse(data, safe=False)


# TODO: Add a decorator to require login
# TODO: Reenable csrf protection
@csrf_exempt
def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = Feedback(
                message=form.cleaned_data["feedback"],
                # TODO: Replace with the actual user
                user=request.user,
                status=Feedback.SUBMITTED,
            )
            feedback.save()

            return home(request)

    return home(request, error="Invalid request")


def view_feedback(request):
    feedback = Feedback.objects.all()
    feedback_data = [
        {
            "id": fb.id,
            "message": fb.message,
            "user": fb.user.username,
            "status": fb.status,
        }
        for fb in feedback
    ]
    return JsonResponse(feedback_data, safe=False)


def update_feedback_status(request):
    if request.method == "POST":
        feedback_id = request.POST.get("feedback_id")
        status = request.POST.get("new_status")
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.status = status
        feedback.save()
        return JsonResponse({"success": True})


def station_data(request):
    # Get the selected date from the query
    selected_date = request.GET.get("datetime", None)
    # Check if date is undefined
    if selected_date == "undefined":
        return JsonResponse(
            {"error": "No data found for the specified date and time"}, status=404
        )
    # Filter the station data to only retrieve data from specified date
    data = StationData.objects.filter(DATE_TIME=selected_date)
    # Check if the data is empty
    if not data.exists():
        # Return an empty JSON response of an error message indicating no data was found
        return JsonResponse(
            {"error": "No data found for the specified date and time"}, status=404
        )
    # Create dictionary of data
    measures = [
        {
            "created_at_timestamp": measure.created_at_timestamp,
            "STATION_CODE": measure.STATION_CODE,
            "STATION_NAME": measure.STATION_NAME,
            "DATE_TIME": measure.DATE_TIME,
            "HOURLY_PRECIPITATION": measure.HOURLY_PRECIPITATION,
            "HOURLY_TEMPERATURE": measure.HOURLY_TEMPERATURE,
            "HOURLY_RELATIVE_HUMIDITY": measure.HOURLY_RELATIVE_HUMIDITY,
            "HOURLY_WIND_SPEED": measure.HOURLY_WIND_SPEED,
            "HOURLY_WIND_DIRECTION": measure.HOURLY_WIND_DIRECTION,
            "HOURLY_WIND_GUST": measure.HOURLY_WIND_GUST,
            "HOURLY_FINE_FUEL_MOISTURE_CODE": measure.HOURLY_FINE_FUEL_MOISTURE_CODE,
            "HOURLY_INITIAL_SPREAD_INDEX": measure.HOURLY_INITIAL_SPREAD_INDEX,
            "HOURLY_FIRE_WEATHER_INDEX": measure.HOURLY_FIRE_WEATHER_INDEX,
            "PRECIPITATION": measure.PRECIPITATION,
            "FINE_FUEL_MOISTURE_CODE": measure.FINE_FUEL_MOISTURE_CODE,
            "INITIAL_SPREAD_INDEX": measure.INITIAL_SPREAD_INDEX,
            "FIRE_WEATHER_INDEX": measure.FIRE_WEATHER_INDEX,
            "DUFF_MOISTURE_CODE": measure.DUFF_MOISTURE_CODE,
            "DROUGHT_CODE": measure.DROUGHT_CODE,
            "BUILDUP_INDEX": measure.BUILDUP_INDEX,
            "DANGER_RATING": measure.DANGER_RATING,
            "RN_1_PLUVIO1": measure.RN_1_PLUVIO1,
            "SNOW_DEPTH": measure.SNOW_DEPTH,
            "SNOW_DEPTH_QUALITY": measure.SNOW_DEPTH_QUALITY,
            "PRECIP_PLUVIO1_STATUS": measure.PRECIP_PLUVIO1_STATUS,
            "PRECIP_PLUVIO1_TOTAL": measure.PRECIP_PLUVIO1_TOTAL,
            "RN_1_PLUVIO2": measure.RN_1_PLUVIO2,
            "PRECIP_PLUVIO2_STATUS": measure.PRECIP_PLUVIO2_STATUS,
            "PRECIP_PLUVIO2_TOTAL": measure.PRECIP_PLUVIO2_TOTAL,
            "RN_1_RIT": measure.RN_1_RIT,
            "PRECIP_RIT_STATUS": measure.PRECIP_RIT_STATUS,
            "PRECIP_RIT_TOTAL": measure.PRECIP_RIT_TOTAL,
            "PRECIP_RGT": measure.PRECIP_RGT,
            "SOLAR_RADIATION_LICOR": measure.SOLAR_RADIATION_LICOR,
            "SOLAR_RADIATION_CM3": measure.SOLAR_RADIATION_CM3,
        }
        for measure in data
    ]
    # Return the data as a json resonse
    return JsonResponse(measures, safe=False)
