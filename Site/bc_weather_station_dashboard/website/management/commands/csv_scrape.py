from django.core.management.base import BaseCommand
import requests
from django.utils import timezone
from datetime import datetime
from website.models import StationData,WeatherStation
import pandas as pd
from django.utils.timezone import make_aware
import tempfile

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
        data = pd.read_csv(filename)
        for index, row in data.iterrows():
            # Convert the date time string to a datetime object
            naive_datetime = datetime.strptime(str(row['DATE_TIME']), "%Y%m%d%H")
            # Make the datetime object timezone aware
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

            # Create a new StationData object or update the existing one
            StationData.objects.get_or_create(**row_data)

    def handle(self, *args, **kwargs)-> None:
        """Handles the command, calls the other methods."""
        # Get the current date in the 'America/Vancouver' timezone
        date = timezone.localtime(timezone.now())

        # Format the date as yyyy-mm-dd
        date_str = date.strftime('%Y-%m-%d')
            
        # Create the URL
        url = f'https://www.for.gov.bc.ca/ftp/HPR/external/!publish/BCWS_DATA_MART/2024/{date_str}.csv'

        # Create a temporary file for the CSV being downloaded
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            # Try to download the CSV
            if self.download_csv(temp_file, url):
                temp_file.seek(0)  # Go to the start of the file
                # Update the model with the data from the CSV
                self.update_model_with_csv(temp_file.name)
                self.stdout.write(self.style.SUCCESS(f'Most current data for {date_str} inserted into the StationData model'))