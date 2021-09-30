from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rooms.tests import RoomsTests
from datetime import datetime, timedelta
import json


class RoomReservationTests(TestCase):
    def Test_create_room_reservation(self, token):
        url = '/api/room_reservations'
        data = {
            "room": RoomsTests().Test_create_room(),
            "start_date": str(datetime.now().date()),
            "end_date": str(datetime.now().date()+ timedelta(days=1))
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["room_reservation"]["id"]

    def Test_chek_in(self, token, reservation_id):
        url = '/api/room_reservations/check_in'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_chek_out(self, token, reservation_id):
        url = '/api/room_reservations/check_in'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_payment_success(self, token, reservation_id):
        url = '/api/room_reservations/payment_success'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_room_reservation_process(self):
        customer_data = {
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@gmail.com",
            "password": "123456"
        }
        customer_token = self.register_user(customer_data, '/api/auth/customer/register')

        receptionist_data = {
            "username": "receptionistTest",
            "first_name": "Receptionist",
            "last_name": "Test",
            "email": "receptionisttest@gmail.com",
            "password": "sep18g21",
            "group": "Receptionist"
        }
        receptionist_token = self.register_user(receptionist_data, '/api/auth/staff/register_test')

        reservation_id = self.Test_create_room_reservation(customer_token)

        self.Test_chek_in(receptionist_token, reservation_id)

        self.Test_payment_success(customer_token, reservation_id)

    def register_user(self, data, url):
        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["token"]
