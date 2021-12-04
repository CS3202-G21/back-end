from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rooms.tests import RoomsTests
from datetime import datetime, timedelta
import json


class RoomReservationTests(TestCase):
    def Test_success_room_reservation_creation(self, token):
        response = self.Test_create_room_reservation(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["room_reservation"]["id"]

    def Test_unauthorized_room_reservation_creation(self, token):
        response = self.Test_create_room_reservation(token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_check_in(self, token, reservation_id):
        response = self.Test_check_in(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_check_in(self, token, reservation_id):
        response = self.Test_check_in(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_invalid_chek_in(self, token, reservation_id):
        response = self.Test_check_in(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_check_out(self, token, reservation_id):
        response = self.Test_check_out(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_check_out(self, token, reservation_id):
        response = self.Test_check_out(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_invalid_chek_out(self, token, reservation_id):
        response = self.Test_check_out(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_payment_success(self, token, reservation_id):
        response = self.Test_payment_success(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_payment_success(self, token, reservation_id):
        response = self.Test_payment_success(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_invalid_payment_success(self, token, reservation_id):
        response = self.Test_payment_success(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_get_room_reservations(self, token):
        response = self.Test_get_room_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_get_room_reservations(self, token):
        response = self.Test_get_room_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_add_review(self, token, reservation_id):
        response = self.Test_add_review(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_add_review(self, token, reservation_id):
        response = self.Test_add_review(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_invalid_add_review(self, token, reservation_id):
        response = self.Test_add_review(token, reservation_id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Test_success_view_room_reservations(self, token):
        response = self.Test_view_room_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_unauthorized_view_room_reservations(self, token):
        response = self.Test_view_room_reservations(token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

        reservation_id = self.Test_success_room_reservation_creation(customer_token)

        self.Test_success_view_room_reservations(receptionist_token)
        self.Test_success_check_in(receptionist_token, reservation_id)
        self.Test_success_payment_success(customer_token, reservation_id)
        self.Test_success_check_out(receptionist_token, reservation_id)
        self.Test_success_add_review(customer_token, reservation_id)
        self.Test_success_get_room_reservations(customer_token)

        # invalid data testing
        self.Test_invalid_chek_in(receptionist_token, reservation_id + 1)
        self.Test_invalid_chek_out(receptionist_token, reservation_id + 1)
        self.Test_invalid_payment_success(customer_token, reservation_id + 1)
        self.Test_invalid_add_review(customer_token, reservation_id + 1)

        chef_data = {
            "username": "chefTest",
            "first_name": "Chef",
            "last_name": "Test",
            "email": "cheftest@gmail.com",
            "password": "sep18g21",
            "group": "Chef"
        }
        chef_token = self.register_user(chef_data, '/api/auth/staff/register_test')

        waiter_data = {
            "username": "waiterTest",
            "first_name": "Waiter",
            "last_name": "Test",
            "email": "waitertest@gmail.com",
            "password": "sep18g21",
            "group": "Waiter"
        }
        waiter_token = self.register_user(waiter_data, '/api/auth/staff/register_test')

        virtual_waiter_data = {
            "username": "virtualWaiter",
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "sep18g21",
            "group": "Virtual Waiter"
        }
        virtual_waiter_token = self.register_user(virtual_waiter_data, '/api/auth/staff/register_test')

        # test unauthorized access
        self.Test_unauthorized_room_reservation_creation(chef_token)
        self.Test_unauthorized_room_reservation_creation(waiter_token)
        self.Test_unauthorized_room_reservation_creation(virtual_waiter_token)

        self.Test_unauthorized_view_room_reservations(customer_token)
        self.Test_unauthorized_view_room_reservations(chef_token)
        self.Test_unauthorized_view_room_reservations(virtual_waiter_token)
        self.Test_unauthorized_view_room_reservations(waiter_token)

        self.Test_unauthorized_check_in(customer_token, reservation_id)
        self.Test_unauthorized_check_in(chef_token, reservation_id)
        self.Test_unauthorized_check_in(virtual_waiter_token, reservation_id)
        self.Test_unauthorized_check_in(waiter_token, reservation_id)

        self.Test_unauthorized_check_out(customer_token, reservation_id)
        self.Test_unauthorized_check_out(chef_token, reservation_id)
        self.Test_unauthorized_check_out(virtual_waiter_token, reservation_id)
        self.Test_unauthorized_check_out(waiter_token, reservation_id)

        self.Test_unauthorized_add_review(receptionist_token, reservation_id)
        self.Test_unauthorized_add_review(chef_token, reservation_id)
        self.Test_unauthorized_add_review(virtual_waiter_token, reservation_id)
        self.Test_unauthorized_add_review(waiter_token, reservation_id)

        self.Test_unauthorized_payment_success(chef_token, reservation_id)
        self.Test_unauthorized_payment_success(virtual_waiter_token, reservation_id)
        self.Test_unauthorized_payment_success(waiter_token, reservation_id)

        self.Test_unauthorized_get_room_reservations(receptionist_token)
        self.Test_unauthorized_get_room_reservations(chef_token)
        self.Test_unauthorized_get_room_reservations(virtual_waiter_token)
        self.Test_unauthorized_get_room_reservations(waiter_token)

    def Test_create_room_reservation(self, token):
        url = '/api/room_reservations'
        data = {
            "room": RoomsTests().Test_create_room(),
            "start_date": str(datetime.now().date()),
            "end_date": str(datetime.now().date() + timedelta(days=1))
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')

        return response

    def Test_check_in(self, token, reservation_id):
        url = '/api/room_reservations/check_in'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        return response

    def Test_check_out(self, token, reservation_id):
        url = '/api/room_reservations/check_out'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        return response

    def Test_payment_success(self, token, reservation_id):
        url = '/api/room_reservations/payment_success'
        data = {
            "reservation_id": reservation_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        return response

    def Test_get_room_reservations(self, token):
        url = '/api/room_reservations'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        return response

    def Test_add_review(self, token, reservation_id):
        url = '/api/room_reservations/add_review'
        data = {
            "reservation_id": reservation_id,
            "customer_review": "Lorem Ipsum"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        return response

    def Test_view_room_reservations(self, token):
        url = '/api/room_reservations/today_reservations'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        return response

    def register_user(self, data, url):
        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["token"]
