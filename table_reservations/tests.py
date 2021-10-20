from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from restaurants.tests import RestaurantsTests
import json


class TableReservationTests(TestCase):
    def Test_success_create_table_reservation(self, token):
        response = self.Test_create_table_reservation(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["table_reservation"]["id"]

    def Test_unauthorized_create_table_reservation(self, token):
        response = self.Test_create_table_reservation(token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_update_customer_arrival(self, token, reservation_id):
        response = self.Test_update_customer_arrival(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_update_customer_arrival(self, token, reservation_id):
        response = self.Test_update_customer_arrival(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_invalid_update_customer_arrival(self, token, reservation_id):
        response = self.Test_update_customer_arrival(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_view_table_reservations(self, token):
        response = self.Test_view_table_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_view_table_reservations(self, token):
        response = self.Test_view_table_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_get_table_reservations(self, token):
        response = self.Test_get_table_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_get_table_reservations(self, token):
        response = self.Test_get_table_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        reservation_id = self.Test_success_create_table_reservation(customer_token)

        self.Test_success_view_table_reservations(waiter_token)
        self.Test_success_update_customer_arrival(waiter_token, reservation_id)
        self.Test_success_get_table_reservations(customer_token)

        # invalid data testing
        self.Test_invalid_update_customer_arrival(waiter_token, reservation_id + 1)

        chef_data = {
            "username": "chefTest",
            "first_name": "Chef",
            "last_name": "Test",
            "email": "cheftest@gmail.com",
            "password": "sep18g21",
            "group": "Chef"
        }
        chef_token = self.register_user(chef_data, '/api/auth/staff/register_test')

        receptionist_data = {
            "username": "receptionistTest",
            "first_name": "Receptionist",
            "last_name": "Test",
            "email": "receptionisttest@gmail.com",
            "password": "sep18g21",
            "group": "Receptionist"
        }
        receptionist_token = self.register_user(receptionist_data, '/api/auth/staff/register_test')

        virtual_waiter_data = {
            "username": "virtualWaiter",
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "sep18g21",
            "group": "Virtual Waiter"
        }
        virtual_waiter_token = self.register_user(virtual_waiter_data, '/api/auth/staff/register_test')

        # unauthorized access testing
        self.Test_unauthorized_create_table_reservation(chef_token)
        self.Test_unauthorized_create_table_reservation(waiter_token)
        self.Test_unauthorized_create_table_reservation(receptionist_token)
        self.Test_unauthorized_create_table_reservation(virtual_waiter_token)

        self.Test_unauthorized_update_customer_arrival(chef_token, reservation_id)
        self.Test_unauthorized_update_customer_arrival(receptionist_token, reservation_id)
        self.Test_unauthorized_update_customer_arrival(customer_token, reservation_id)
        self.Test_unauthorized_update_customer_arrival(virtual_waiter_token, reservation_id)

        self.Test_unauthorized_get_table_reservations(chef_token)
        self.Test_unauthorized_get_table_reservations(waiter_token)
        self.Test_unauthorized_get_table_reservations(receptionist_token)
        self.Test_unauthorized_get_table_reservations(virtual_waiter_token)

        self.Test_unauthorized_view_table_reservations(chef_token)
        self.Test_unauthorized_view_table_reservations(customer_token)
        self.Test_unauthorized_view_table_reservations(receptionist_token)
        self.Test_unauthorized_view_table_reservations(virtual_waiter_token)

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
        return response

    def Test_update_customer_arrival(self, token, reservation_id):
        url = '/api/table_reservations/arrival'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        return response

    def Test_view_table_reservations(self, token):
        url = '/api/table_reservations/today_reservations'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        return response

    def Test_get_table_reservations(self, token):
        url = '/api/table_reservations'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        return response

    def register_user(self, data, url):
        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["token"]
