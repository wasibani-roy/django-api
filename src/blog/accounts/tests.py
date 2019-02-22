from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from postings.models import BlogPost

User = get_user_model()
paylaod_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

class AccountAPITestCase(APITestCase):
    def setUp(self):
        user_object = User(username="testuser", email="testuser@gmail.com")
        user_object.set_password("testuser") #sets password for our user
        user_object.save()

    def test_user_registration(self):
        data = {
            "username":"testuser1",
            "email": "testuser1@gmail.com",
            "email2": "testuser1@gmail.com",
            "password": "testuser1"
        }
        url = api_reverse("register")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_non_matching_email(self):
        data = {
            "username":"testuser1",
            "email": "testuser1@gmail.com",
            "email2": "testuser@gmail.com",
            "password": "testuser1"
        }
        url = api_reverse("register")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_already_used_email(self):
        data = {
            "username":"testuser1",
            "email": "testuser@gmail.com",
            "email2": "testuser@gmail.com",
            "password": "testuser1"
        }
        url = api_reverse("register")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        data = {
            "username":"testuser1",
            "email": "testuser1@gmail.com",
            "email2": "testuser1@gmail.com",
            "password": "testuser1"
        }
        url = api_reverse("register")
        self.client.post(url, data, format='json')
        login_data = {
            "username": "testuser1",
            "password": "testuser1"
        }
        url = api_reverse("login")
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_credentials(self):
        data = {
            "username":"testuser1",
            "email": "testuser1@gmail.com",
            "email2": "testuser1@gmail.com",
            "password": "testuser1"
        }
        url = api_reverse("register")
        self.client.post(url, data, format='json')
        login_data = {
            "username": "testuser1",
            "password": "tes"
        }
        url = api_reverse("login")
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

