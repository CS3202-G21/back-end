from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework import status
from .models import MenuItem
from restaurants.tests import RestaurantsTests

import json


class MenuItemsTests(TestCase):
    def Test_create_menu_item(self):
        menu_item = {
            "title": "test",
            "restaurant": RestaurantsTests().Test_create_restaurant(),
            "description": "Lorem Ipsum",
            "price": 1000.0,
            "type": MenuItem.menu_types[0][0],
            "photo_main": self.temporary_image()
        }
        url = '/api/menu_items/'

        client = Client()
        response = client.post(url, menu_item)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return json.loads(response.content.decode("utf-8"))["id"]

    def test_get_menu_items(self):
        id = self.Test_create_menu_item()

        url = '/api/menu_items/'+str(id)+'/'

        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["id"], id)

        url = '/api/menu_items/'
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def temporary_image(self):
        bts = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())