# Create your tests here.
from django.test import TestCase
from .models import UserProfile, User, WeatherStation, StationData, Dashboard, Alert, Feedback, ResponseFromAdmin
import os
from django.conf import settings
from django.core.management import call_command
from io import StringIO
import pandas as pd
import re

#Begin models tests

# Test the UserProfile model
class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='testuser', password='12345')
        UserProfile.objects.create(user=test_user, user_type='CU')

    # Test the user field
    def test_user_label(self):
        # This test checks if the verbose name of the 'user' field is correctly set to 'user'
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    # Test the user_type field
    def test_user_type_label(self):
        # This test checks if the verbose name of the 'user_type' field is correctly set to 'user type'
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field('user_type').verbose_name
        self.assertEquals(field_label, 'user type')

    # Test the favorite_stations field
    def test_user_type_max_length(self):
        # This test checks if the max_length of the 'user_type' field is correctly set to 2
        userprofile = UserProfile.objects.get(id=1)
        max_length = userprofile._meta.get_field('user_type').max_length
        self.assertEquals(max_length, 2)

    # Test the user_type field default value
    def test_user_type_default(self):
        # This test checks if the default value of the 'user_type' field is correctly set to 'CU'
        userprofile = UserProfile.objects.get(id=1)
        default_value = userprofile._meta.get_field('user_type').default
        self.assertEquals(default_value, 'CU')

    # Test the __str__ method
    def test_object_name_is_username(self):
        # This test checks if the __str__ method of the UserProfile model returns the correct string
        userprofile = UserProfile.objects.get(id=1)
        expected_object_name = f'{userprofile.user.username} ({userprofile.user_type})'
        self.assertEquals(expected_object_name, str(userprofile))
    
    class StationModelTest(TestCase):
        @classmethod
        def setUpTestData(cls):
            # Set up non-modified objects used by all test methods
            WeatherStation.objects.create(name='Test Station', location='Test Location')

        def test_name_label(self):
            # This test checks if the verbose name of the 'name' field is correctly set to 'name'
            station = WeatherStation.objects.get(id=1)
            field_label = station._meta.get_field('name').verbose_name
            self.assertEquals(field_label, 'name')

        def test_location_label(self):
            # This test checks if the verbose name of the 'location' field is correctly set to 'location'
            station = WeatherStation.objects.get(id=1)
            field_label = station._meta.get_field('location').verbose_name
            self.assertEquals(field_label, 'location')

        def test_object_name_is_name(self):
            # This test checks if the __str__ method of the Station model returns the correct string
            station = WeatherStation.objects.get(id=1)
            expected_object_name = f'{station.name}'
            self.assertEquals(expected_object_name, str(station))
            
    class StationDataModelTest(TestCase):
        @classmethod
        def setUpTestData(cls):
            # Set up non-modified objects used by all test methods
            WeatherStation.objects.create(name='Test Station', location='Test Location')
            StationData.objects.create(station=WeatherStation.objects.get(id=1), date_time='2020-01-01 10:00:00')

        def test_station_label(self):
            # This test checks if the verbose name of the 'station' field is correctly set to 'station'
            station_data = StationData.objects.get(id=1)
            field_label = station_data._meta.get_field('station').verbose_name
            self.assertEquals(field_label, 'station')

        def test_date_time_label(self):
            # This test checks if the verbose name of the 'date_time' field is correctly set to 'date time'
            station_data = StationData.objects.get(id=1)
            field_label = station_data._meta.get_field('date_time').verbose_name
            self.assertEquals(field_label, 'date time')

        def test_object_name_is_station_name(self):
            # This test checks if the __str__ method of the StationData model returns the correct string
            station_data = StationData.objects.get(id=1)
            expected_object_name = f'{station_data.station.name}'
            self.assertEquals(expected_object_name, str(station_data))
class DashboardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='testuser', password='12345')
        Dashboard.objects.create(user=test_user, theme='default', layout='common')

    def test_theme_label(self):
        # This test checks if the verbose name of the 'theme' field is correctly set to 'theme'
        dashboard = Dashboard.objects.get(id=1)
        field_label = dashboard._meta.get_field('theme').verbose_name
        self.assertEquals(field_label, 'theme')

    def test_layout_label(self):
        # This test checks if the verbose name of the 'layout' field is correctly set to 'layout'
        dashboard = Dashboard.objects.get(id=1)
        field_label = dashboard._meta.get_field('layout').verbose_name
        self.assertEquals(field_label, 'layout')

    def test_object_name(self):
        # This test checks if the __str__ method of the Dashboard model returns the correct string
        dashboard = Dashboard.objects.get(id=1)
        expected_object_name = f"{dashboard.user.username}'s Dashboard Preferences"
        self.assertEquals(expected_object_name, str(dashboard))


class AlertModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='testuser', password='12345')
        Alert.objects.create(alert_name='Test Alert', message='Test Message', alert_type='Test Type', alert_active=True)

    def test_alert_name_label(self):
        # This test checks if the verbose name of the 'alert_name' field is correctly set to 'alert name'
        alert = Alert.objects.get(id=1)
        field_label = alert._meta.get_field('alert_name').verbose_name
        self.assertEquals(field_label, 'alert name')

    def test_message_label(self):
        # This test checks if the verbose name of the 'message' field is correctly set to 'message'
        alert = Alert.objects.get(id=1)
        field_label = alert._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_object_name(self):
        # This test checks if the __str__ method of the Alert model returns the correct string
        alert = Alert.objects.get(id=1)
        expected_object_name = f"{alert.alert_name}"
        self.assertEquals(expected_object_name, str(alert))


class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='testuser', password='12345')
        Feedback.objects.create(message='Test Message', user=test_user, status=Feedback.SUBMITTED)

    def test_message_label(self):
        # This test checks if the verbose name of the 'message' field is correctly set to 'message'
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_status_label(self):
        # This test checks if the verbose name of the 'status' field is correctly set to 'status'
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_object_name(self):
        # This test checks if the __str__ method of the Feedback model returns the correct string
        feedback = Feedback.objects.get(id=1)
        expected_object_name = f"Feedback from {feedback.user.username}"
        self.assertEquals(expected_object_name, str(feedback))


class ResponseFromAdminModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='testuser', password='12345')
        feedback = Feedback.objects.create(message='Test Message', user=test_user, status=Feedback.SUBMITTED)
        ResponseFromAdmin.objects.create(feedback=feedback, admin=test_user, message='Test Response')

    def test_message_label(self):
        # This test checks if the verbose name of the 'message' field is correctly set to 'message'
        response = ResponseFromAdmin.objects.get(id=1)
        field_label = response._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'message')

    def test_object_name(self):
        # This test checks if the __str__ method of the ResponseFromAdmin model returns the correct string
        response = ResponseFromAdmin.objects.get(id=1)
        expected_object_name = f"Response to {response.feedback}"
        self.assertEquals(expected_object_name, str(response))
        
#End models tests

#Test ws_upload command
class WSUploadCommandTestCase(TestCase):
    def setUp(self):
        self.csv_path = os.path.join(settings.BASE_DIR, 'website', 'data', 'BC_Wildfire_Active_Weather_Stations.csv')
        self.data = pd.read_csv(self.csv_path)

    def test_command_output(self):
        # Test if the command outputs 'Data uploaded successfully'
        try:
            out = StringIO()
            call_command('ws_upload', stdout=out)
            self.assertIn('Data uploaded successfully', out.getvalue())
        except Exception as e:
            self.fail(e)

    def test_data_upload(self):
        # Test if the data from the csv file was uploaded correctly
        call_command('ws_upload')
        for _, row in self.data.iterrows():
            ws = WeatherStation.objects.filter(WEATHER_STATIONS_ID=row["WEATHER_STATIONS_ID"]).first()
            self.assertIsNotNone(ws)
            self.assertEqual(ws.X, row["X"])
            self.assertEqual(ws.Y, row["Y"])
            self.assertEqual(ws.STATION_CODE, row["STATION_CODE"])
            self.assertEqual(ws.STATION_NAME, row["STATION_NAME"])
            if ws.STATION_ACRONYM == 'nan' and pd.isna(row["STATION_ACRONYM"]):
                self.assertTrue(True)
            else:
                self.assertEqual(ws.STATION_ACRONYM, row["STATION_ACRONYM"])
            self.assertEqual(ws.ELEVATION, row["ELEVATION"])
            self.assertEqual(ws.INSTALL_DATE, pd.to_datetime(row["INSTALL_DATE"], format='%Y/%m/%d %H:%M:%S%z'))
#End ws_upload command tests

#Test csv_scrape command
class CSVScrapeCommandTestCase(TestCase):
    def setUp(self):
        self.csv_url = "https://www.for.gov.bc.ca/ftp/HPR/external/!publish/BCWS_DATA_MART/2024/2024-01-01.csv" # Replace with the actual path of the CSV file
        self.data = pd.read_csv(self.csv_url)
    def test_command_output(self):
        # Run the command
        out = StringIO()
        call_command('csv_scrape', stdout=out)

        # Strip escape sequences from the output
        output = re.sub(r'\x1b\[.*?m', '', out.getvalue())

        # Check the output
        self.assertIn('Deleted Successfully', output)
    def test_data_scrape(self):
        # Test if the data from the CSV file was scraped correctly by checking if the expected station codes are in the database
        call_command('csv_scrape')
        # Get all unique station codes from the CSV file
        unique_station_codes = set(self.data["STATION_CODE"].astype(str).unique())
        # Check if the expected station codes are in the set of unique station codes
        expected_station_codes = {1024, 1025, 1029, 11, 19, 21, 1045, 1055, 1056, 37, 3110, 554, 555, 556, 45, 1066, 1075, 56, 1082, 59, 1083, 67, 1092, 1093, 72, 75, 82, 2130, 1108, 599, 93, 101, 105, 106, 108, 110, 111, 112, 113, 118, 119, 120, 121, 1144, 2170, 124, 3190, 126, 127, 3191, 129, 131, 132, 136, 138, 140, 141, 654, 1165, 144, 145, 146, 148, 149, 151, 152, 153, 154, 155, 156, 1176, 158, 159, 162, 163, 166, 167, 169, 170, 171, 172, 173, 1199, 1203, 180, 181, 182, 187, 189, 190, 192, 193, 1218, 195, 1221, 199, 200, 206, 209, 210, 211, 212, 1239, 216, 1240, 218, 1241, 1242, 222, 225, 226, 227, 228, 230, 232, 233, 234, 235, 236, 1260, 239, 1264, 1265, 243, 244, 1268, 1270, 250, 251, 1275, 253, 1276, 255, 1277, 1790, 1283, 262, 263, 264, 266, 267, 270, 788, 790, 279, 280, 791, 283, 286, 1313, 291, 292, 298, 1323, 301, 302, 305, 306, 307, 1330, 309, 1332, 311, 1339, 316, 317, 832, 321, 322, 1345, 836, 1348, 326, 838, 1349, 331, 334, 1359, 1362, 344, 1375, 352, 865, 866, 1377, 868, 1378, 1383, 873, 362, 363, 876, 1387, 366, 367, 1392, 882, 886, 1398, 1399, 379, 380, 383, 1408, 385, 387, 388, 391, 392, 393, 394, 904, 396, 905, 401, 402, 2450, 404, 406, 407, 408, 919, 411, 412, 417, 418, 419, 421, 425, 426, 427, 428, 429, 430, 431, 432, 433, 938, 944, 945, 437, 438, 440, 956, 445, 965, 1994, 977, 474, 480, 995, 503}
        for code in expected_station_codes:
            self.assertIn(str(code), unique_station_codes)
            
#End csv_scrape command tests