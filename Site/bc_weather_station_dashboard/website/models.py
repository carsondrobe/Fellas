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
    station_code = models.IntegerField()
    station_name = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    hourly_precipitation = models.FloatField()
    hourly_temperature = models.FloatField()
    hourly_relative_humidity = models.FloatField()
    hourly_wind_speed = models.FloatField()
    hourly_wind_direction = models.FloatField()
    hourly_wind_gust = models.FloatField()
    hourly_fine_fuel_moisture_code = models.FloatField()
    hourly_initial_spread_index = models.FloatField()
    hourly_fire_weather_index = models.FloatField()
    precipitation = models.FloatField()
    fine_fuel_moisture_code = models.FloatField()
    initial_spread_index = models.FloatField()
    fire_weather_index = models.FloatField()
    duff_moisture_code = models.FloatField()
    drought_code = models.FloatField()
    buildup_index = models.FloatField()
    danger_rating = models.FloatField()
    rn_1_pluvio1 = models.FloatField()
    snow_depth = models.FloatField()
    snow_depth_quality = models.FloatField()
    precip_pluvio1_status = models.FloatField()
    precip_pluvio1_total = models.FloatField()
    rn_1_pluvio2 = models.FloatField()
    precip_pluvio2_status = models.FloatField()
    precip_pluvio2_total = models.FloatField()
    rn_1_rit = models.FloatField()
    precip_rit_status = models.FloatField()
    precip_rit_total = models.FloatField()
    precip_rgt = models.FloatField()
    solar_radiation_licor = models.FloatField()
    solar_radiation_cm3 = models.FloatField()

    def __str__(self):
        return self.station_name