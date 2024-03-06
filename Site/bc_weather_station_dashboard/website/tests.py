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
        Alert.objects.create(
            alert_name="Test Alert",
            message="Test Message",
            alert_type="Test Type",
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
                pd.to_datetime(row["INSTALL_DATE"], format="%Y/%m/%d %H:%M:%S%z"),
            )


# End ws_upload command tests


# Test the submit_feedback view

from django.urls import reverse
from website.forms import FeedbackForm


class SubmitFeedbackTests(TestCase):
    def test_submit_feedback_valid_form(self):
        url = reverse("submit_feedback")
        data = {"feedback": "This is a test feedback"}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, 302
        )  # Check if it redirects to the home page

        # TODO: Add assertions to check if the feedback is saved to the database

    def test_submit_feedback_invalid_form(self):
        url = reverse("submit_feedback")
        data = {}  # Empty data to make the form invalid
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, 200
        )  # Check if it renders the weather.html template

        # TODO: Add assertions to check if the form is passed to the template context

    def test_submit_feedback_get_request(self):
        url = reverse("submit_feedback")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200
        )  # Check if it renders the weather.html template

        # TODO: Add assertions to check if the form is passed to the template context

        form = response.context["feedback_form"]
        self.assertIsInstance(
            form, FeedbackForm
        )  # Check if the form is an instance of FeedbackForm
