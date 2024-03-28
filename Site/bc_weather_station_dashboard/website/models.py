from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# make sure to run "python manage.py makemigrations" and "python manage.py migrate" after making changes to models.py
# This will update the database schema to reflect the changes made to the models.py file
# Note: Django pluralizes the model name when creating the table in the database (e.g. User -> Users, WeatherStation -> WeatherStations)


# The User model is used to store user information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, unique=True)
    COMMON_USER = "CU"
    FIRE_STAFF = "FS"
    USER_TYPE_CHOICES = [
        (COMMON_USER, "Common user"),
        (FIRE_STAFF, "Fire related staff"),
    ]

    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPE_CHOICES,
        default=COMMON_USER,
    )
    favorite_stations = models.ManyToManyField("WeatherStation", related_name="users")

    def __str__(self):
        return self.user.username + " (" + self.user_type + ")"


# The WeatherStation model is used to store weather station information
# Note: Follows namming convention of csv file
class WeatherStation(models.Model):
    X = models.FloatField()  # longitude
    Y = models.FloatField()  # latitude
    WEATHER_STATIONS_ID = models.IntegerField()
    STATION_CODE = models.IntegerField(default=0)
    STATION_NAME = models.CharField(default="Station", max_length=200)
    STATION_ACRONYM = models.CharField(default="ST", max_length=200)
    ELEVATION = models.IntegerField(default=0)
    INSTALL_DATE = models.DateTimeField()

    def __str__(self):
        return self.STATION_NAME + " (" + str(self.STATION_CODE) + ")"


# The StationData model is used to store station data
# Note: Follows namming convention of csv file
class StationData(models.Model):
    station = models.ForeignKey(
        WeatherStation, on_delete=models.CASCADE, related_name="station_data", default=0
    )
    created_at_timestamp = models.DateTimeField(auto_now_add=True)
    STATION_CODE = models.IntegerField()
    STATION_NAME = models.CharField(max_length=200)
    DATE_TIME = models.DateTimeField()
    HOURLY_PRECIPITATION = models.FloatField()
    HOURLY_TEMPERATURE = models.FloatField()
    HOURLY_RELATIVE_HUMIDITY = models.FloatField()
    HOURLY_WIND_SPEED = models.FloatField()
    HOURLY_WIND_DIRECTION = models.FloatField()
    HOURLY_WIND_GUST = models.FloatField()
    HOURLY_FINE_FUEL_MOISTURE_CODE = models.FloatField()
    HOURLY_INITIAL_SPREAD_INDEX = models.FloatField()
    HOURLY_FIRE_WEATHER_INDEX = models.FloatField()
    PRECIPITATION = models.FloatField()
    FINE_FUEL_MOISTURE_CODE = models.FloatField()
    INITIAL_SPREAD_INDEX = models.FloatField()
    FIRE_WEATHER_INDEX = models.FloatField()
    DUFF_MOISTURE_CODE = models.FloatField()
    DROUGHT_CODE = models.FloatField()
    BUILDUP_INDEX = models.FloatField()
    DANGER_RATING = models.FloatField()
    RN_1_PLUVIO1 = models.FloatField()
    SNOW_DEPTH = models.FloatField()
    SNOW_DEPTH_QUALITY = models.FloatField()
    PRECIP_PLUVIO1_STATUS = models.FloatField()
    PRECIP_PLUVIO1_TOTAL = models.FloatField()
    RN_1_PLUVIO2 = models.FloatField()
    PRECIP_PLUVIO2_STATUS = models.FloatField()
    PRECIP_PLUVIO2_TOTAL = models.FloatField()
    RN_1_RIT = models.FloatField()
    PRECIP_RIT_STATUS = models.FloatField()
    PRECIP_RIT_TOTAL = models.FloatField()
    PRECIP_RGT = models.FloatField()
    SOLAR_RADIATION_LICOR = models.FloatField()
    SOLAR_RADIATION_CM3 = models.FloatField()

    def __str__(self):
        return self.STATION_NAME


# The Dashboard model is used to store user type information for dashboard order showing station data
class Dashboard(models.Model):
    LAYOUT_CHOICES = [
        ("firefighter", "Firefighter Layout"),
        ("common", "Common Layout"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=200, default="default")
    layout = models.CharField(max_length=200, choices=LAYOUT_CHOICES, default="common")

    def __str__(self):
        return self.user.username + "'s Dashboard Preferences"


class Alert(models.Model):
    user = models.ManyToManyField(User)
    alert_name = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    alert_type = models.CharField(max_length=200)
    station_data = models.ManyToManyField(StationData)
    alert_active = models.BooleanField()

    def __str__(self):
        return self.alert_name


class Feedback(models.Model):
    # Status choices
    SUBMITTED = "SUB"
    IN_REVIEW = "REV"
    ADDRESSED = "ADD"
    STATUS_CHOICES = [
        (SUBMITTED, "Submitted"),
        (IN_REVIEW, "In Review"),
        (ADDRESSED, "Addressed"),
    ]

    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=SUBMITTED,
    )

    def __str__(self):
        return f"Feedback from {self.user.username}"


class ResponseFromAdmin(models.Model):
    feedback = models.OneToOneField(
        Feedback, on_delete=models.CASCADE, related_name="response"
    )
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    message = models.TextField()

    def __str__(self):
        return f"Response to {self.feedback}"
