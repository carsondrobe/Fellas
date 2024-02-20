from django.db import models

# Create your models here.

# make sure to run "python manage.py makemigrations" and "python manage.py migrate" after making changes to models.py
# This will update the database schema to reflect the changes made to the models.py file
# Note: Django pluralizes the model name when creating the table in the database (e.g. User -> Users, WeatherStation -> WeatherStations)


# The User model is used to store user information
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name + " " + self.last_name

# The WeatherStation model is used to store weather station information
class WeatherStation(models.Model):
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