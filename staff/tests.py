from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json


class StaffUserTests(TestCase):
    def Test_register_staff(self, group):
        url = '/api/auth/staff/register_test'
        data = {
            "username": "testing",
            "first_name": "Test",
            "last_name": "Test",
            "email": "test@gmail.com",
            "password": "sep18g21",
            "group": group
        }

        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_login_staff(self):
        url = '/api/auth/staff/login'
        data = {
            "username": "testing",
            "password": "sep18g21"
        }

        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["token"]

    def Test_get_user(self, token):
        url = '/api/auth/staff/user'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_customer_then_login_customer(self):
        self.Test_register_staff("Chef")
        token = self.Test_login_staff()
        self.Test_get_user(token)
