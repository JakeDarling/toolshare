from django.db import models

class Shed(models.Model):
    name = models.CharField(max_length=30)
    zipcode = models.IntegerField()
    address_one = models.CharField(max_length=254)
    address_two = models.CharField(max_length=254, blank=True)
    owner_id = models.IntegerField()
    owner_string = models.CharField(max_length=100)
    private = models.BooleanField(True, False)
