import warnings
from datetime import timedelta
from django.core.management.base import BaseCommand
import requests
from django.utils import timezone
from datetime import date
from datetime import datetime, timedelta
from website.models import StationData,WeatherStation
import pandas as pd
import os
class Command(BaseCommand):
    help = 'Manually download current day CSV data and update StationData model to run use the command: python manage.py csv_scrape.'

    def download_csv(self, temp_file, url) -> bool:
        """Downloads a CSV file and writes it to a temporary file."""
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            temp_file.write(response.content)
            self.stdout.write(self.style.SUCCESS(f"Downloaded file: {temp_file.name}"))
            return True
        else:
            self.stdout.write(self.style.ERROR(f"Failed to download file. Today's data is unavailable right now. {url}"))
            return False

    def update_model_with_csv(self, filename) -> None:
        """Updates the StationData model with data from a CSV file."""
        warnings.filterwarnings('ignore')
        data = pd.read_csv(filename)
        for index, row in data.iterrows():
            # Convert the date time string to a datetime object
            naive_datetime = datetime.strptime(str(row['DATE_TIME']), "%Y%m%d%H")
            row['DATE_TIME'] = naive_datetime

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

            # Create a new StationData object or update the existing one
            StationData.objects.get_or_create(**row_data)

    def handle(self, *args, **kwargs) -> None:
        """Handles the command, calls the other methods. You can change the date range here."""
        # Create a date range for when you want to scrape the data
        start_date = (datetime.today() - timedelta(days=2)).date()  # Change the start date
        end_date = date.today()  # Change the end date
        delta = timedelta(days=1)
        dates = []
        while start_date <= end_date:
            dates.append(start_date)
            start_date += delta

        # Loop over the dates
        for date_current in dates:
            # Format the date as yyyy-mm-dd
            date_str = date_current.strftime('%Y-%m-%d')
            # Get the year from the date
            year = date_current.strftime('%Y')

            # Create the URL and filename
            url = f'https://www.for.gov.bc.ca/ftp/HPR/external/!publish/BCWS_DATA_MART/{year}/{date_str}.csv'
            filename = f'{date_str}.csv'

            try:
                # Open a temporary file
                with open(filename, 'wb') as temp_file:
                    # Try to download the CSV
                    if self.download_csv(temp_file, url):
                        self.update_model_with_csv(filename)
                self.stdout.write(self.style.SUCCESS(f'Data inserted into the model for {filename}'))
            finally:
                # Delete the CSV file after model updated
                if os.path.exists(filename):
                    os.remove(filename)
                    self.stdout.write(self.style.SUCCESS(f'File {filename} Deleted Successfully'))