from django.db import models
from djmoney.models.fields import MoneyField
from accounts.models import User
import secrets
import string

def generate_custom_id():
    segment_length = 5
    num_segments = 3
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    segments = [''.join(secrets.choice(characters) for _ in range(segment_length)) for _ in range(num_segments)]
    return '-'.join(segments)

class Coordinates(models.Model):
    id = models.CharField(primary_key=True, max_length=17, default=generate_custom_id, editable=False, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f'{self.latitude}, {self.longitude}'
    
class Address(models.Model):
    id = models.CharField(primary_key=True, max_length=17, default=generate_custom_id, editable=False, unique=True)
    street_1 = models.CharField(max_length=1000, null=True, blank=True)
    street_2 = models.CharField(max_length=1000, null=True, blank=True)
    street_3 = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    province = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=1000, null=True, blank=True)
    coordinates = models.ForeignKey(Coordinates, on_delete=models.SET_NULL, null=True, blank=True, related_name="address_coordinates")

    def __str__(self):
        return f'{self.street_1}, {self.street_2}'

class Property(models.Model):
    id = models.CharField(primary_key=True, max_length=17, default=generate_custom_id, editable=False, unique=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="property_landlord")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True, related_name="property_address")
    number_of_vacant = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    inclusion = models.CharField(max_length=255, null=True, blank=True)
    rent = MoneyField(max_digits=14, decimal_places=2, default_currency='PHP', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.landlord.username
    
class Room(models.Model):
    tenant = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    is_vacant = models.BooleanField(default=True)

    def __str__(self):
        return self.tenant.username
