from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Restaurant(models.Model):
    # restaurant status enum
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'
    MAINTENANCE = 'maintenance'
    room_statuses = (
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable'),
        (MAINTENANCE, 'Maintenance')
    )

    title = models.CharField(max_length=255)
    floor_number = models.IntegerField()
    type = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=room_statuses, default=AVAILABLE)
    number_of_tables = models.IntegerField()
    max_number_of_people_for_reservation = models.IntegerField(default=50, blank=True)  # max number of people that can be pre-booked for a restaurant for a specific meal time in a specific day
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    photo_main = models.ImageField(upload_to='photos/restaurants/main')
    photo_1 = models.ImageField(upload_to='photos/restaurants/other', blank=True)
    photo_2 = models.ImageField(upload_to='photos/restaurants/other', blank=True)
    photo_3 = models.ImageField(upload_to='photos/restaurants/other', blank=True)
    date_added = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.title)
