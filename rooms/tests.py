from django.test import Client, TestCase
from rest_framework import status
from room_types.tests import RoomTypesTests
import json


class RoomsTests(TestCase):
    def Test_create_room(self):
        restaurant = {
            "room_number": 101,
            "floor_number": 1,
            "type": RoomTypesTests().Test_create_room_type()
        }
        url = '/api/rooms/'

        client = Client()
        response = client.post(url, restaurant)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return json.loads(response.content.decode("utf-8"))["id"]

    def test_get_rooms(self):
        id = self.Test_create_room()

        url = '/api/rooms/'+str(id)+'/'

        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["id"], id)

        url = '/api/rooms/'
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)