from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework import status
import json


class RoomTypesTests(TestCase):
    def Test_create_room_type(self):
        room_type = {
            "title": "Test Type",
            "price": 1,
            "number_of_adults": 1,
            "number_of_beds": 1,
            "description": "Lorem Ipsum",
            "photo_main": self.temporary_image()
        }
        url = '/api/room_types/'

        client = Client()
        response = client.post(url, room_type)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return json.loads(response.content.decode("utf-8"))["id"]

    def test_get_room_types(self):
        id = self.Test_create_room_type()

        url = '/api/room_types/'+str(id)+'/'

        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["id"], id)

        url = '/api/room_types/'
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def temporary_image(self):
        bts = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())