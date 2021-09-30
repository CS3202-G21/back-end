from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from restaurants.tests import RestaurantsTests
import json


class TableReservationTests(TestCase):
    def Test_create_table_reservation(self, token):
        url = '/api/table_reservations'
        data = {
            "restaurant": RestaurantsTests().Test_create_restaurant(),
            "meal_time": 2,
            "reserved_date": str(datetime.now().date()),
            "num_of_people": 4
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["table_reservation"]["id"]

    def Test_update_customer_arrival(self, token, reservation_id):
        url = '/api/table_reservations/arrival'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_view_table_reservations(self, token):
        url = '/api/table_reservations/today_reservations'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_table_reservation_process(self):
        customer_data = {
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@gmail.com",
            "password": "123456"
        }
        customer_token = self.register_user(customer_data, '/api/auth/customer/register')

        waiter_data = {
            "username": "waiterTest",
            "first_name": "Waiter",
            "last_name": "Test",
            "email": "waitertest@gmail.com",
            "password": "sep18g21",
            "group": "Waiter"
        }
        waiter_token = self.register_user(waiter_data, '/api/auth/staff/register_test')

        reservation_id = self.Test_create_table_reservation(customer_token)

        self.Test_view_table_reservations(waiter_token)

        self.Test_update_customer_arrival(waiter_token, reservation_id)

    def register_user(self, data, url):
        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["token"]
