from django.core.management.base import BaseCommand
from website.models import WeatherStation
import pandas as pd
import os
from django.conf import settings
from django.utils import timezone

class Command(BaseCommand):
    help = 'Upload CSV info about weather stations to WeatherStation model'

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'website', 'data', 'BC_Wildfire_Active_Weather_Stations.csv')
        data = pd.read_csv(csv_path)
        
        for _, row in data.iterrows():
            install_date = pd.to_datetime(row["INSTALL_DATE"], format='%Y/%m/%d %H:%M:%S%z')
            install_date_naive = timezone.make_naive(install_date)

            weather_station = WeatherStation(
                X = row["X"],
                Y = row["Y"],
                WEATHER_STATIONS_ID = row["WEATHER_STATIONS_ID"],
                STATION_CODE = row["STATION_CODE"],
                STATION_NAME = row["STATION_NAME"],
                STATION_ACRONYM = row["STATION_ACRONYM"],
                ELEVATION = row["ELEVATION"],
                INSTALL_DATE = install_date_naive
            )
            weather_station.save()

        self.stdout.write(self.style.SUCCESS('Data uploaded successfully'))