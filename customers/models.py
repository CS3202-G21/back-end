from django.db import models
from django.contrib.auth.models import User


class CustomerDetails(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    contact_no = models.IntegerField(blank=True)
    profile_picture = models.ImageField(upload_to='photos/customers', blank=True)

    def __str__(self):
        return str(self.id)
