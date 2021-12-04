from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework import status
from .models import MenuItem
from menu_items.tests import MenuItemsTests

import json


class SpecialOffersTests(TestCase):
    def Test_create_special_offer(self):
        special_offer = {
            "title": "test",
            "menu_item": MenuItemsTests().Test_create_menu_item(),
            "number_of_items": 5,
            "discount": 10,
            "description": "Lorem Ipsum",
            "photo_main": self.temporary_image()
        }
        url = '/api/special_offers/'

        client = Client()
        response = client.post(url, special_offer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return json.loads(response.content.decode("utf-8"))["id"]

    def test_get_special_offer(self):
        id = self.Test_create_special_offer()

        url = '/api/special_offers/'+str(id)+'/'

        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["id"], id)

        url = '/api/special_offers/'
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def temporary_image(self):
        bts = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())