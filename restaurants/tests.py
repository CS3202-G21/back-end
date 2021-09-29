# from django.test import Client, TestCase
# from rest_framework import status
#
#
# class RestaurantsTests(TestCase):
#     def test_get_restaurants(self):
#         restaurant = {
#             "title": "Curry Mahal",
#             "floor_number": 1,
#             "type": "Indian",
#             "number_of_tables": 30,
#             "max_number_of_people_for_reservation": 100,
#             "lunch": True,
#             "dinner": True,
#             "description": "Lorem Ipsum"
#         }
#         url = '/api/restaurants/'
#
#         client = Client()
#         # response = client.post(url, restaurant)
#         # print(response.status_code, response.content)
#
#         url = '/api/restaurants'
#         response = client.get(url)
#         print(response.content)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)