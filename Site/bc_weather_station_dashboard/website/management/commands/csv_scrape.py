from django.core.management.base import BaseCommand
import requests
import time
from pytz import timezone
from datetime import datetime, timedelta
from website.models import WeatherStation
import pandas as pd

class Command(BaseCommand):
    help = 'Download CSV data and update WeatherStation model'

    def download_csv(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded file: {filename}")
        else:
            print(f"Failed to download file. Today's data is unavailable right now. {url}")

    def update_model_with_csv(self, filename):
        data = pd.read_csv(filename)
        for index, row in data.iterrows():
            row['DATE_TIME'] = datetime.strptime(str(row['DATE_TIME']), "%Y%m%d%H")
        
            # Replace None or NaN values with a default value
            row_data = row.to_dict()
            for key, value in row_data.items():
                if pd.isnull(value):
                    row_data[key] = 0

            WeatherStation.objects.create(**row_data)

    def handle(self, *args, **kwargs):
        date = datetime.now(timezone('America/Vancouver'))

        while True:
            # Format the date as yyyy-mm-dd
            date_str = date.strftime('%Y-%m-%d')
            
            # Create the URL and filename
            url = f'https://www.for.gov.bc.ca/ftp/HPR/external/!publish/BCWS_DATA_MART/2024/{date_str}.csv'
            filename = f'{date_str}.csv'
            
            # Try to download the CSV
            self.download_csv(url, filename)
            self.update_model_with_csv(filename)
            time.sleep(14400)
