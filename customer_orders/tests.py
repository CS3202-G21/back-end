from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework import status
from restaurants.tests import RestaurantsTests
import json


class CustomerOrderTests(TestCase):
    def Test_create_order(self, token):
        url = '/api/order'
        data = {
            "customer": "johndoe",
            "restaurant": RestaurantsTests().Test_create_restaurant(),
            "table_no": 1,
            "total_price": 3000,
            "menu_items": {"2": 3, "3": 2},
            "special_offers": {"1": 2}
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["order"]["id"]

    def Test_order_update(self, token, order_id):
        url = '/api/order/update'
        data = {
            "order_id": order_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_payment_success(self, token, order_id):
        url = '/api/order/payment_success'
        data = {
            "order_id": order_id
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_get_customer_orders(self, token):
        url = '/api/order'

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def Test_add_review(self, token, order_id):
        url = '/api/order/add_review'
        data = {
            "order_id": order_id,
            "customer": "johndoe",
            "customer_review": "Lorem Ipsum"
        }

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_order_process(self):
        customer_data = {
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "jdoe@gmail.com",
            "password": "123456"
        }
        customer_token = self.register_user(customer_data, '/api/auth/customer/register')

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

        order_id = self.Test_create_order(virtual_waiter_token)

        self.Test_order_update(chef_token, order_id)
        self.Test_order_update(chef_token, order_id)
        self.Test_order_update(chef_token, order_id)

        self.Test_order_update(waiter_token, order_id)
        self.Test_order_update(waiter_token, order_id)

        self.Test_payment_success(virtual_waiter_token, order_id)

        self.Test_add_review(virtual_waiter_token, order_id)

        self.Test_get_customer_orders(customer_token)


    def register_user(self, data, url):
        client = Client()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content.decode("utf-8"))["token"]
