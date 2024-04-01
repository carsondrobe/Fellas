import warnings
from datetime import timedelta
from django.core.management.base import BaseCommand
import requests
from datetime import date
from datetime import datetime
from website.models import StationData, WeatherStation, UserProfile, Alert
import pandas as pd
import os
from twilio.rest import Client
from django.conf import settings

# Twilio setup
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

def send_sms_alert(phone_number, message):
    """Sends an SMS alert to a given phone number."""
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

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

            # Check for extreme weather conditions for the current row
            self.check_for_extreme_conditions(row_data)
            
    def check_for_extreme_conditions(self, row_data):
        """Checks for extreme weather conditions and sends an SMS alert if any are found."""
        # Check for extreme weather conditions
        extreme_conditions = []
        if row_data['HOURLY_TEMPERATURE'] < -20:
            extreme_conditions.append(f"Current temperature is {row_data['HOURLY_TEMPERATURE']}°C. Please stay warm!")
        elif row_data['HOURLY_TEMPERATURE'] > 40:
            extreme_conditions.append(f"Current temperature is {row_data['HOURLY_TEMPERATURE']}°C. Please stay cool!")

        if row_data['HOURLY_WIND_SPEED'] > 50 and row_data['HOURLY_PRECIPITATION'] > 50:
            extreme_conditions.append(f"Current Wind Speed is: {row_data['HOURLY_WIND_SPEED']}km/h and Precipitation is: {row_data['HOURLY_PRECIPITATION']}mm these are both high.")

        if extreme_conditions:
            # Fetch the phone numbers from the User Profile model
            user_profiles = UserProfile.objects.all()
            for user_profile in user_profiles:
                phone_number = user_profile.phone_number
                message = "Extreme weather conditions detected: " + " ".join(extreme_conditions) + " Please stay safe."
                send_sms_alert(phone_number, message)

            # Create a new Alert object and save it to the database
            alert = Alert(
                alert_name='Extreme Weather Conditions',
                message=message,
                alert_type='Weather',
                station=WeatherStation.objects.get(STATION_NAME=row_data['STATION_NAME']),
                alert_active=True
            )
            alert.save()
                    
    def handle(self, *args, **kwargs) -> None:
        """Handles the command, calls the other methods. You can change the date range here."""
        # Create a date range for when you want to scrape the data
        start_date = date.today() - timedelta(days=1)  # Yesterday's date #date(2024, 3, 19) # Change the start date (make sure this start_date and end_date are in the same year)
        end_date = date.today() # Change the end date
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