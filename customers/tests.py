from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json


class CustomerUserTests(TestCase):
    def Test_register_customer(self):
        url = '/api/auth/customer/register'
        data = {
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@gmail.com",
            "password": "123456"
        }

        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_login_customer(self):
        url = '/api/auth/customer/login'
        data = {
            "username": "johndoe",
            "password": "123456"
        }

        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["token"]

    def Test_get_user(self, token):
        url = '/api/auth/customer/user'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_customer_then_login_customer(self):
        self.Test_register_customer()
        token = self.Test_login_customer()
        self.Test_get_user(token)