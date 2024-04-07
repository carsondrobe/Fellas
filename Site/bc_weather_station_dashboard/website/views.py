from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import FeedbackForm
from django.http import JsonResponse
from .models import WeatherStation, Feedback, StationData, UserProfile, Alert
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.conf import settings
from .models import UserProfile
from .forms import UserProfileForm
from django.db.models import Max
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import io
import urllib, base64
import numpy as np
import datetime


current_page = "weather"
def home(request, **kwargs):
    try:
        user_type = request.user.userprofile.user_type
    except:
        user_type = "CU"

    context = {"user_type": user_type}
    if current_page == "weather":
        return weather(request, **kwargs, **context)
    elif current_page == "fire":
        return fire(request, **kwargs, **context)
    else:
        raise ValueError("Invalid page", current_page)


def weather(request, **kwargs):
    global current_page
    current_page = "weather"

    kwargs["template_name"] = "weather"
    return render(request, "weather.html", kwargs)


def display_fav_button(request):
    if request.method == "POST":
        station_code = request.POST.get("station_code")
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            weather_station = WeatherStation.objects.get(STATION_CODE=station_code)
            if weather_station in user_profile.favorite_stations.all():
                return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def fire(request, **kwargs):
    global current_page
    current_page = "fire"
    kwargs["template_name"] = "fire"
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
            return home(request)
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
    phone_number = request.POST.get("phone_number")
    user_type = request.POST.get("user_type")
    password = request.POST.get("password")
    if not username or not email or not password or not phone_number:
        return HttpResponse("Please fill in all fields", status=400)

    # Create the user
    user = User.objects.create_user(username, email, password)
    user.save()

    # Creates the "user profile" model with information
    user_profile = UserProfile(
        user=user, phone_number=phone_number, user_type=user_type
    )
    user_profile.save()

    # Logs user in
    login(request, user)

    # Send SMS after successful registration
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Hey {username}!\n Thank you for registering with the BC Weather & Wildfire Dashboard for important weather alerts. -Fellas",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number,
    )

    return home(request)


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
    # Check if the request is for the latest data
    latest = request.GET.get("latest", "false").lower() == "true"
    station_code = request.GET.get("station_code", None)

    # Handle request for the latest data
    if latest:
        queryset = StationData.objects
        if station_code:
            queryset = queryset.filter(STATION_CODE=station_code)
        latest_entry = queryset.aggregate(latest_date=Max("DATE_TIME"))["latest_date"]
        if latest_entry is None:
            return JsonResponse({"error": "No data available"}, status=404)
        data = queryset.filter(DATE_TIME=latest_entry)

    else:
        # Get the selected date from the query
        selected_date = request.GET.get("datetime", None)
        if selected_date is None or selected_date == "undefined":
            return JsonResponse(
                {"error": "No data found for the specified date and time"}, status=404
            )

        # Filter the station data to only retrieve data from the specified date and station code
        queryset = StationData.objects.filter(DATE_TIME=selected_date)
        if station_code:
            queryset = queryset.filter(STATION_CODE=station_code)
        data = queryset

    if not data.exists():
        return JsonResponse({"error": "No data found"}, status=404)
    # Create dictionary of data
    measures = [
        {
            "created_at_timestamp": measure.created_at_timestamp,
            "STATION_CODE": measure.STATION_CODE,
            "STATION_NAME": measure.STATION_NAME,
            "DATE_TIME": measure.DATE_TIME.strftime("%Y-%m-%d %H:%M:%S"),
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


@login_required
def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    non_addressed_feedbacks = request.user.feedbacks.exclude(status="ADD")
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            request.user.email = request.POST.get("email")
            request.user.save()
            return redirect("view_profile")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(
        request,
        "profile.html",
        {
            "form": form,
            "user_profile": user_profile,
            "non_addressed_feedbacks": non_addressed_feedbacks,
        },
    )


def add_to_favourites(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            station_code = request.POST.get("station_code")
            station = WeatherStation.objects.get(STATION_CODE=station_code)
            request.user.userprofile.favorite_stations.add(station)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def view_favourites(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not logged in"}, status=200)
    favourites = request.user.userprofile.favorite_stations.all()
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
        for station in favourites
    ]
    return JsonResponse(data, safe=False)


def delete_favourite(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            station_name = request.POST.get("station_name")
            station = WeatherStation.objects.get(STATION_NAME=station_name)
            request.user.userprofile.favorite_stations.remove(station)
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@login_required
def alerts_view(request):
    alerts = Alert.objects.select_related("station").all()
    data = [
        {
            "alert_name": alert.alert_name,
            "message": alert.message,
            "alert_type": alert.alert_type,
            "station_id": alert.station.id if alert.station else None,
            "station_name": alert.station.STATION_NAME if alert.station else None,
            "alert_active": alert.alert_active,
        }
        for alert in alerts
    ]
    return JsonResponse(data, safe=False)


### Predictions
# Receives request from view_predictions.js
# This function generates a plot
# and returns the URI of the plot to the frontend. Essentially passing back an encoded image
# to the frontend.


def predictions(request):
    matplotlib.use("agg")  # IMPORTANT for Django to use matplotlib

    # Example data for scatter plot
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 3, 2, 4, 3])

    # Set figure size here (width, height) in inches
    plt.figure(figsize=(10, 6))  # Example size: 10 inches by 6 inches

    # Create a scatter plot
    plt.scatter(x, y)

    # Adding title
    plt.title("Tomorrow's Prediction")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(
        buf, format="png", bbox_inches="tight"
    )  # Ensuring no clipping of the figure
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return JsonResponse({"uri": uri})
