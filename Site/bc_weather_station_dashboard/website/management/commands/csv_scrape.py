from django.core.management.base import BaseCommand
import requests
from pytz import timezone
from datetime import datetime
from website.models import StationData  
from website.models import WeatherStation
import pandas as pd
import os
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = 'Download CSV data and update WeatherStation model'

    def download_csv(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            self.stdout.write(self.style.SUCCESS(f"Downloaded file: {filename}"))
        else:
            print(f"Failed to download file. Today's data is unavailable right now. {url}")

    def update_model_with_csv(self, filename):
        data = pd.read_csv(filename)
        for index, row in data.iterrows():
            naive_datetime = datetime.strptime(str(row['DATE_TIME']), "%Y%m%d%H")
            aware_datetime = make_aware(naive_datetime)
            row['DATE_TIME'] = aware_datetime

            # Replace None or NaN values with a default value
            row_data = row.to_dict()
            for key, value in row_data.items():
                if pd.isnull(value):
                    row_data[key] = 0

            # Try to get the corresponding WeatherStation instance
            try:
                station = WeatherStation.objects.get(STATION_CODE=row_data['STATION_CODE'])
            except WeatherStation.DoesNotExist:
                # If the WeatherStation does not exist, skip to the next iteration
                continue

            # Set the station field of the StationData instance
            row_data['station'] = station

            StationData.objects.get_or_create(**row_data)

    def handle(self, *args, **kwargs):
        date = datetime.now(timezone('America/Vancouver'))

        # Format the date as yyyy-mm-dd
        date_str = date.strftime('%Y-%m-%d')
            
        # Create the URL and filename
        url = f'https://www.for.gov.bc.ca/ftp/HPR/external/!publish/BCWS_DATA_MART/2024/{date_str}.csv'
        filename = f'{date_str}.csv'

        # Try to download the CSV
        self.download_csv(url, filename)
        self.update_model_with_csv(filename)

        try:
            self.update_model_with_csv(filename)
            self.stdout.write(self.style.SUCCESS('Data inserted into the model'))
        finally:
            # Delete the CSV file after model updated
            if os.path.exists(filename):
                os.remove(filename)
                self.stdout.write(self.style.SUCCESS('File Delted Successfully'))