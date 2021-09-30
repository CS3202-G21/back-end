from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework import status
import json


class RestaurantsTests(TestCase):
    def Test_create_restaurant(self):
        restaurant = {
            "title": "Curry Mahal",
            "floor_number": 1,
            "type": "Indian",
            "number_of_tables": 30,
            "max_number_of_people_for_reservation": 100,
            "lunch": True,
            "dinner": True,
            "description": "Lorem Ipsum",
            "photo_main": self.temporary_image()
        }
        url = '/api/restaurants/'

        client = Client()
        response = client.post(url, restaurant)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return json.loads(response.content.decode("utf-8"))["id"]


    # def test_get_restaurants(self):
    #     url = '/api/restaurants'
    #
    #     client = Client()
    #     response = client.get(url)
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    def temporary_image(self):
        bts = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())