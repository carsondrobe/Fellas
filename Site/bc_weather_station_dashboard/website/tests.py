# Create your tests here.
from django.test import TestCase
from .models import (
    UserProfile,
    User,
    WeatherStation,
    StationData,
    Dashboard,
    Alert,
    Feedback,
    ResponseFromAdmin,
)
import os
from django.conf import settings
from django.core.management import call_command
from io import StringIO
import pandas as pd
from django.urls import reverse
from django.contrib.auth.models import User
import re
from website.forms import FeedbackForm
from django.test import TestCase, Client, RequestFactory
from website.views import add_to_favourites
from django.utils import timezone
from .models import UserProfile
from datetime import date
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
from website.management.commands import csv_scrape
import csv
import pandas as pd

# Begin models tests


# Test the UserProfile model
class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username="testuser", password="12345")
        UserProfile.objects.create(user=test_user, user_type="CU")

    # Test the user field
    def test_user_label(self):
        # This test checks if the verbose name of the 'user' field is correctly set to 'user'
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "user")

    # Test the user_type field
    def test_user_type_label(self):
        # This test checks if the verbose name of the 'user_type' field is correctly set to 'user type'
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field("user_type").verbose_name
        self.assertEquals(field_label, "user type")

    # Test the favorite_stations field
    def test_user_type_max_length(self):
        # This test checks if the max_length of the 'user_type' field is correctly set to 2
        userprofile = UserProfile.objects.get(id=1)
        max_length = userprofile._meta.get_field("user_type").max_length
        self.assertEquals(max_length, 2)

    # Test the user_type field default value
    def test_user_type_default(self):
        # This test checks if the default value of the 'user_type' field is correctly set to 'CU'
        userprofile = UserProfile.objects.get(id=1)
        default_value = userprofile._meta.get_field("user_type").default
        self.assertEquals(default_value, "CU")

    # Test the __str__ method
    def test_object_name_is_username(self):
        # This test checks if the __str__ method of the UserProfile model returns the correct string
        userprofile = UserProfile.objects.get(id=1)
        expected_object_name = f"{userprofile.user.username} ({userprofile.user_type})"
        self.assertEquals(expected_object_name, str(userprofile))

    class StationModelTest(TestCase):
        @classmethod
        def setUpTestData(cls):
            # Set up non-modified objects used by all test methods
            WeatherStation.objects.create(name="Test Station", location="Test Location")

        def test_name_label(self):
            # This test checks if the verbose name of the 'name' field is correctly set to 'name'
            station = WeatherStation.objects.get(id=1)
            field_label = station._meta.get_field("name").verbose_name
            self.assertEquals(field_label, "name")

        def test_location_label(self):
            # This test checks if the verbose name of the 'location' field is correctly set to 'location'
            station = WeatherStation.objects.get(id=1)
            field_label = station._meta.get_field("location").verbose_name
            self.assertEquals(field_label, "location")

        def test_object_name_is_name(self):
            # This test checks if the __str__ method of the Station model returns the correct string
            station = WeatherStation.objects.get(id=1)
            expected_object_name = f"{station.name}"
            self.assertEquals(expected_object_name, str(station))

    class StationDataModelTest(TestCase):
        @classmethod
        def setUpTestData(cls):
            # Set up non-modified objects used by all test methods
            WeatherStation.objects.create(name="Test Station", location="Test Location")
            StationData.objects.create(
                station=WeatherStation.objects.get(id=1),
                date_time="2020-01-01 10:00:00",
            )

        def test_station_label(self):
            # This test checks if the verbose name of the 'station' field is correctly set to 'station'
            station_data = StationData.objects.get(id=1)
            field_label = station_data._meta.get_field("station").verbose_name
            self.assertEquals(field_label, "station")

        def test_date_time_label(self):
            # This test checks if the verbose name of the 'date_time' field is correctly set to 'date time'
            station_data = StationData.objects.get(id=1)
            field_label = station_data._meta.get_field("date_time").verbose_name
            self.assertEquals(field_label, "date time")

        def test_object_name_is_station_name(self):
            # This test checks if the __str__ method of the StationData model returns the correct string
            station_data = StationData.objects.get(id=1)
            expected_object_name = f"{station_data.station.name}"
            self.assertEquals(expected_object_name, str(station_data))


class DashboardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username="testuser", password="12345")
        Dashboard.objects.create(user=test_user, theme="default", layout="common")

    def test_theme_label(self):
        # This test checks if the verbose name of the 'theme' field is correctly set to 'theme'
        dashboard = Dashboard.objects.get(id=1)
        field_label = dashboard._meta.get_field("theme").verbose_name
        self.assertEquals(field_label, "theme")

    def test_layout_label(self):
        # This test checks if the verbose name of the 'layout' field is correctly set to 'layout'
        dashboard = Dashboard.objects.get(id=1)
        field_label = dashboard._meta.get_field("layout").verbose_name
        self.assertEquals(field_label, "layout")

    def test_object_name(self):
        # This test checks if the __str__ method of the Dashboard model returns the correct string
        dashboard = Dashboard.objects.get(id=1)
        expected_object_name = f"{dashboard.user.username}'s Dashboard Preferences"
        self.assertEquals(expected_object_name, str(dashboard))


class AlertModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_station = WeatherStation.objects.create(
            X=0, 
            Y=0, 
            WEATHER_STATIONS_ID=1, 
            STATION_CODE=123, 
            STATION_NAME="Test Station", 
            STATION_ACRONYM="TS", 
            ELEVATION=100, 
            INSTALL_DATE=date.today()
        )
        Alert.objects.create(
            alert_name="Test Alert",
            message="Test Message",
            alert_type="Test Type",
            station=test_station,
            alert_active=True,
        )
    def test_alert_name_label(self):
        # This test checks if the verbose name of the 'alert_name' field is correctly set to 'alert name'
        alert = Alert.objects.get(id=1)
        field_label = alert._meta.get_field("alert_name").verbose_name
        self.assertEquals(field_label, "alert name")

    def test_message_label(self):
        # This test checks if the verbose name of the 'message' field is correctly set to 'message'
        alert = Alert.objects.get(id=1)
        field_label = alert._meta.get_field("message").verbose_name
        self.assertEquals(field_label, "message")

    def test_object_name(self):
        # This test checks if the __str__ method of the Alert model returns the correct string
        alert = Alert.objects.get(id=1)
        expected_object_name = f"{alert.alert_name}"
        self.assertEquals(expected_object_name, str(alert))

class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username="testuser", password="12345")
        Feedback.objects.create(
            message="Test Message", user=test_user, status=Feedback.SUBMITTED
        )

    def test_message_label(self):
        # This test checks if the verbose name of the 'message' field is correctly set to 'message'
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field("message").verbose_name
        self.assertEquals(field_label, "message")

    def test_status_label(self):
        # This test checks if the verbose name of the 'status' field is correctly set to 'status'
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field("status").verbose_name
        self.assertEquals(field_label, "status")

    def test_object_name(self):
        # This test checks if the __str__ method of the Feedback model returns the correct string
        feedback = Feedback.objects.get(id=1)
        expected_object_name = f"Feedback from {feedback.user.username}"
        self.assertEquals(expected_object_name, str(feedback))


class ResponseFromAdminModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username="testuser", password="12345")
        feedback = Feedback.objects.create(
            message="Test Message", user=test_user, status=Feedback.SUBMITTED
        )
        ResponseFromAdmin.objects.create(
            feedback=feedback, admin=test_user, message="Test Response"
        )

    def test_message_label(self):
        # This test checks if the verbose name of the 'message' field is correctly set to 'message'
        response = ResponseFromAdmin.objects.get(id=1)
        field_label = response._meta.get_field("message").verbose_name
        self.assertEquals(field_label, "message")

    def test_object_name(self):
        # This test checks if the __str__ method of the ResponseFromAdmin model returns the correct string
        response = ResponseFromAdmin.objects.get(id=1)
        expected_object_name = f"Response to {response.feedback}"
        self.assertEquals(expected_object_name, str(response))


# End models tests


# Test ws_upload command
class WSUploadCommandTestCase(TestCase):
    def setUp(self):
        self.csv_path = os.path.join(
            settings.BASE_DIR,
            "website",
            "data",
            "BC_Wildfire_Active_Weather_Stations.csv",
        )
        self.data = pd.read_csv(self.csv_path)

    def test_command_output(self):
        # Test if the command outputs 'Data uploaded successfully'
        try:
            out = StringIO()
            call_command("ws_upload", stdout=out)
            self.assertIn("Data uploaded successfully", out.getvalue())
        except Exception as e:
            self.fail(e)

    def test_data_upload(self):
        # Test if the data from the csv file was uploaded correctly
        call_command("ws_upload")
        for _, row in self.data.iterrows():
            ws = WeatherStation.objects.filter(
                WEATHER_STATIONS_ID=row["WEATHER_STATIONS_ID"]
            ).first()
            self.assertIsNotNone(ws)
            self.assertEqual(ws.X, row["X"])
            self.assertEqual(ws.Y, row["Y"])
            self.assertEqual(ws.STATION_CODE, row["STATION_CODE"])
            self.assertEqual(ws.STATION_NAME, row["STATION_NAME"])
            if ws.STATION_ACRONYM == "nan" and pd.isna(row["STATION_ACRONYM"]):
                self.assertTrue(True)
            else:
                self.assertEqual(ws.STATION_ACRONYM, row["STATION_ACRONYM"])
            self.assertEqual(ws.ELEVATION, row["ELEVATION"])
            self.assertEqual(
                ws.INSTALL_DATE,
                timezone.make_naive(pd.to_datetime(row["INSTALL_DATE"], format="%Y/%m/%d %H:%M:%S%z")),
            )


# End ws_upload command tests


# Test the submit_feedback view


class SubmitFeedbackTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_submit_feedback_valid(self):
        # Create the Feedback object specifically for this test
        self.feedback = Feedback.objects.create(
            user=self.user, message="This is a test feedback", status=Feedback.SUBMITTED
        )

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        feedback_data = {"feedback": "This is a test feedback"}

        # Simulate a POST request to submit feedback
        response = self.client.post(reverse("submit_feedback"), data=feedback_data)

        # Check if the response is a direct to home
        self.assertEqual(response.status_code, 200)

        # Since feedback is created in the test, check for updated values
        updated_feedback = Feedback.objects.get(pk=self.feedback.pk)

        self.assertEqual(updated_feedback.message, feedback_data["feedback"])
        self.assertEqual(updated_feedback.user, self.user)
        self.assertEqual(updated_feedback.status, Feedback.SUBMITTED)

    def test_submit_feedback_invalid(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Simulate a POST request with invalid data
        response = self.client.post(reverse("submit_feedback"), data={})

        # Check if the response is a redirect
        self.assertEqual(response.status_code, 200)

        # Check that no feedback is saved in the database
        self.assertEqual(Feedback.objects.count(), 0)

    def test_submit_feedback_get_request(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Simulate a GET request
        response = self.client.get(reverse("submit_feedback"))

        # Check if the response is a redirect
        self.assertEqual(response.status_code, 200)

        # Check that no feedback is saved in the database
        self.assertEqual(Feedback.objects.count(), 0)


class ViewFeedbackTestCase(TestCase):
    def test_view_feedback_success(self):
        # Create a test user and feedback
        user = User.objects.create_user(username="testuser", password="testpassword")
        feedback = Feedback.objects.create(
            message="Some feedback", user=user, status="new"
        )

        # Make a request
        response = self.client.get(reverse("view_feedback"))
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)  # Should have one feedback item
        self.assertEqual(response.json()[0]["message"], "Some feedback")

    def test_view_feedback_empty(self):
        response = self.client.get(reverse("view_feedback"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class UpdateFeedbackStatusTestCase(TestCase):
    def test_update_status_success(self):
        user = User.objects.create_user(username="testuser")
        feedback = Feedback.objects.create(
            message="Some feedback", user=user, status="new"
        )

        response = self.client.post(
            reverse("update_feedback_status"),  # Replace if needed
            data={"feedback_id": feedback.id, "new_status": "resolved"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

        # Reload feedback object to check if it's updated
        updated_feedback = Feedback.objects.get(id=feedback.id)
        self.assertEqual(updated_feedback.status, "resolved")


class AddFavouriteStationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.station = WeatherStation.objects.create(
            X=1.0,
            Y=1.0,
            WEATHER_STATIONS_ID=1,
            STATION_CODE=1,
            STATION_NAME="Test Station",
            STATION_ACRONYM="TS",
            ELEVATION=1,
            INSTALL_DATE=timezone.now(),
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.url = reverse("add_to_favourites")

    def test_add_to_favourites_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(self.url, {"station_code": 1})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        self.assertIn(self.station, self.user.userprofile.favorite_stations.all())

    def test_add_to_favourites_unauthenticated(self):
        response = self.client.post(self.url, {"station_code": 1})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": False})

    def test_add_to_favourites_get_request(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": False})


class ViewFavouritesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user)
        self.station = WeatherStation.objects.create(
            X=1.0,
            Y=1.0,
            WEATHER_STATIONS_ID=1,
            STATION_CODE=1,
            STATION_NAME="Test Station",
            STATION_ACRONYM="TS",
            ELEVATION=1,
            INSTALL_DATE=timezone.now(),
        )
        self.profile.favorite_stations.add(self.station)

    def test_view_favourites(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/view_favourites/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": 1,
                    "code": 1,
                    "name": "Test Station",
                    "acronym": "TS",
                    "latitude": 1.0,
                    "longitude": 1.0,
                    "elevation": 1,
                    "install_date": self.station.INSTALL_DATE.strftime("%Y-%m-%d"),
                }
            ],
        )


class DeleteFavouriteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user)
        self.station = WeatherStation.objects.create(
            X=1.0,
            Y=1.0,
            WEATHER_STATIONS_ID=1,
            STATION_CODE=1,
            STATION_NAME="Test Station",
            STATION_ACRONYM="TS",
            ELEVATION=1,
            INSTALL_DATE=timezone.now(),
        )
        self.profile.favorite_stations.add(self.station)

    def test_delete_favourite(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            "/delete_favourite/", {"station_name": "Test Station"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        self.assertNotIn(self.station, self.user.userprofile.favorite_stations.all())


class ViewFavouriteButtonTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user)
        self.station = WeatherStation.objects.create(
            X=1.0,
            Y=1.0,
            WEATHER_STATIONS_ID=1,
            STATION_CODE=1,
            STATION_NAME="Test Station",
            STATION_ACRONYM="TS",
            ELEVATION=1,
            INSTALL_DATE=timezone.now(),
        )
        self.profile.favorite_stations.add(self.station)

    def test_display_fav_button(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post("/display_fav_button/", {"station_code": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})


# Profile page tests in views.py
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client.login(username="testuser", password="12345")

    def test_view_profile(self):
        response = self.client.get(reverse("view_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

class CsvScrapeTest(TestCase):
    def setUp(self):
        # Create a WeatherStation instance
        from datetime import date

        self.station = WeatherStation.objects.create(
            X=1.0,
            Y=1.0,
            WEATHER_STATIONS_ID=1,
            STATION_CODE=1,
            STATION_NAME="Test Station",
            STATION_ACRONYM="TS",
            ELEVATION=1,
            INSTALL_DATE=timezone.now(),
        )
        # Create a UserProfile instance
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, phone_number='+12503066199')
        # Create a StationData instance
        self.station_data = StationData.objects.create(
            station=self.station,
            created_at_timestamp=datetime.now(),
            STATION_CODE=1,
            STATION_NAME='TEST_NAME',
            DATE_TIME=datetime.now(),
            HOURLY_PRECIPITATION=0.0,
            HOURLY_TEMPERATURE=0.0,
            HOURLY_RELATIVE_HUMIDITY=0.0,
            HOURLY_WIND_SPEED=0.0,
            HOURLY_WIND_DIRECTION=0.0,
            HOURLY_WIND_GUST=0.0,
            HOURLY_FINE_FUEL_MOISTURE_CODE=0.0,
            HOURLY_INITIAL_SPREAD_INDEX=0.0,
            HOURLY_FIRE_WEATHER_INDEX=0.0,
            PRECIPITATION=0.0,
            FINE_FUEL_MOISTURE_CODE=0.0,
            INITIAL_SPREAD_INDEX=0.0,
            FIRE_WEATHER_INDEX=0.0,
            DUFF_MOISTURE_CODE=0.0,
            DROUGHT_CODE=0.0,
            BUILDUP_INDEX=0.0,
            DANGER_RATING=0.0,
            RN_1_PLUVIO1=0.0,
            SNOW_DEPTH=0.0,
            SNOW_DEPTH_QUALITY=0.0,
            PRECIP_PLUVIO1_STATUS=0.0,
            PRECIP_PLUVIO1_TOTAL=0.0,
            RN_1_PLUVIO2=0.0,
            PRECIP_PLUVIO2_STATUS=0.0,
            PRECIP_PLUVIO2_TOTAL=0.0,
            RN_1_RIT=0.0,
            PRECIP_RIT_STATUS=0.0,
            PRECIP_RIT_TOTAL=0.0,
            PRECIP_RGT=0.0,
            SOLAR_RADIATION_LICOR=0.0,
            SOLAR_RADIATION_CM3=0.0
        )

    @patch('website.management.commands.csv_scrape.send_sms_alert')
    def test_check_for_extreme_conditions_favorite_station(self, mock_send_sms_alert):
        # Add station to user's favorite stations
        self.user_profile.favorite_stations.add(self.station)

        # Create a Command instance
        command = csv_scrape.Command()

        # Create a row_data dictionary
        row_data = {
            'DATE_TIME': '2022-01-01 00:00:00',
            'STATION_CODE': 1,
            'HOURLY_TEMPERATURE': 50,
            'HOURLY_WIND_SPEED': 60,
            'HOURLY_PRECIPITATION': 70,
            'STATION_NAME': 'Test Station',
            'station': self.station
        }

        # Call the check_for_extreme_conditions method
        command.check_for_extreme_conditions(row_data)

        # Check that an SMS alert was sent
        self.assertTrue(mock_send_sms_alert.called)
        if mock_send_sms_alert.called:
            print("Message sent:", mock_send_sms_alert.call_args[0][1])

        # Check that an Alert instance was created
        self.assertEqual(Alert.objects.count(), 1)
        alert = Alert.objects.first()
        self.assertEqual(alert.alert_name, 'Extreme Weather Conditions')
        self.assertEqual(alert.alert_type, 'Weather')
        self.assertEqual(alert.station, self.station)
        self.assertTrue(alert.alert_active)

    @patch('website.management.commands.csv_scrape.send_sms_alert')
    def test_check_for_extreme_conditions_not_favorite_station(self, mock_send_sms_alert):
        # Create a Command instance
        command = csv_scrape.Command()

        # Create a row_data dictionary
        row_data = {
            'DATE_TIME': '2022-01-01 00:00:00',
            'STATION_CODE': 1,
            'HOURLY_TEMPERATURE': 50,
            'HOURLY_WIND_SPEED': 60,
            'HOURLY_PRECIPITATION': 70,
            'STATION_NAME': 'Test Station',
            'station': self.station
        }

        # Call the check_for_extreme_conditions method
        command.check_for_extreme_conditions(row_data)

        # Check that an SMS alert was not sent
        self.assertFalse(mock_send_sms_alert.called)
        if mock_send_sms_alert.called:
            print("Message sent:", mock_send_sms_alert.call_args[0][1])

        # Check that an Alert instance was not created
        self.assertEqual(Alert.objects.count(), 0)
        
    @patch('website.management.commands.csv_scrape.Command.download_csv')
    @patch('website.management.commands.csv_scrape.Command.update_model_with_csv')
    def test_handle(self, mock_update_model_with_csv, mock_download_csv):
        # Create a Command instance
        command = csv_scrape.Command()

        # Mock the return value of download_csv
        mock_download_csv.return_value = True

        # Call the handle method
        command.handle()

        # Check that download_csv and update_model_with_csv were called
        self.assertEqual(mock_download_csv.call_count, 1)
        mock_update_model_with_csv.assert_called_once()
        
    @patch('pandas.read_csv')
    def test_update_model_with_csv(self, mock_read_csv):
        # Create a Command instance
        command = csv_scrape.Command()

        # Mock the return value of pd.read_csv
        mock_read_csv.return_value = pd.DataFrame([{
            'STATION_CODE': 1,
            'STATION_NAME': 'TEST_NAME',
            'DATE_TIME': '2024033100',
            'HOURLY_PRECIPITATION': 0.0,
            'HOURLY_TEMPERATURE': 0.0,
            'HOURLY_RELATIVE_HUMIDITY': 0.0,
            'HOURLY_WIND_SPEED': 0.0,
            'HOURLY_WIND_DIRECTION': 0.0,
            'HOURLY_WIND_GUST': 0.0,
            'HOURLY_FINE_FUEL_MOISTURE_CODE': 0.0,
            'HOURLY_INITIAL_SPREAD_INDEX': 0.0,
            'HOURLY_FIRE_WEATHER_INDEX': 0.0,
            'PRECIPITATION': 0.0,
            'FINE_FUEL_MOISTURE_CODE': 0.0,
            'INITIAL_SPREAD_INDEX': 0.0,
            'FIRE_WEATHER_INDEX': 0.0,
            'DUFF_MOISTURE_CODE': 0.0,
            'DROUGHT_CODE': 0.0,
            'BUILDUP_INDEX': 0.0,
            'DANGER_RATING': 0.0,
            'RN_1_PLUVIO1': 0.0,
            'SNOW_DEPTH': 0.0,
            'SNOW_DEPTH_QUALITY': 0.0,
            'PRECIP_PLUVIO1_STATUS': 0.0,
            'PRECIP_PLUVIO1_TOTAL': 0.0,
            'RN_1_PLUVIO2': 0.0,
            'PRECIP_PLUVIO2_STATUS': 0.0,
            'PRECIP_PLUVIO2_TOTAL': 0.0,
            'RN_1_RIT': 0.0,
            'PRECIP_RIT_STATUS': 0.0,
            'PRECIP_RIT_TOTAL': 0.0,
            'PRECIP_RGT': 0.0,
            'SOLAR_RADIATION_LICOR': 0.0,
            'SOLAR_RADIATION_CM3': 0.0,
        }])

        # Call the update_model_with_csv method
        command.update_model_with_csv('testfile.csv')

        # Check that pd.read_csv was called with the correct arguments
        mock_read_csv.assert_called_once_with('testfile.csv')

    @patch('website.management.commands.csv_scrape.Command.download_csv')
    @patch('website.management.commands.csv_scrape.Command.update_model_with_csv')
    def test_handle(self, mock_update_model_with_csv, mock_download_csv):
        # Create a Command instance
        command = csv_scrape.Command()

        # Mock the return value of download_csv
        mock_download_csv.return_value = True

        # Call the handle method
        command.handle()

        # Check that download_csv was called twice and update_model_with_csv was called twice
        self.assertEqual(mock_download_csv.call_count, 2)
        self.assertEqual(mock_update_model_with_csv.call_count, 2)