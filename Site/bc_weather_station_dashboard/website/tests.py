from django.test import TestCase
from django.urls import reverse
from django.test import Client

# Create your tests here.

class LoginTests(TestCase):
    def test_login_view_invalid_data(self):
        client = Client()
        response = client.post(reverse('login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'Please fill in all fields')

    def test_login_view_valid_data(self):
        client = Client()
        response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'Login form submitted successfully')
