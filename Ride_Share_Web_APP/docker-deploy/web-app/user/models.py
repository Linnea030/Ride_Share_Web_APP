#operation on database
from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False, null=True, blank=True)


class Vehicle(models.Model):
    id = models.BigAutoField(primary_key=True)
    plate_num = models.CharField(max_length=256)
    vehicle_type = models.CharField(max_length=256, null=True, blank=True)
    max_capacity = models.IntegerField(default=4)
    special_info = models.CharField(max_length=256, null=True, blank=True)
    #owner = models.OneToOneField(User, on_delete=models.CASCADE)


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    arrival_time = models.DateTimeField()
    destination = models.CharField(max_length=256)
    capacity = models.IntegerField(default=0, null=True, blank=True)
    vehicle_type = models.CharField(max_length=128, null=True, blank=True)
    is_shared = models.BooleanField(default=False)

    STATUS = (
        (0, 'open'),
        (1, 'confirmed'),
        (2, 'completed'),
    )
    status = models.IntegerField(choices=STATUS, default=0)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    driver = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='driver')
    sharer = models.ManyToManyField(User, blank=True, related_name='sharer')

    special_info = models.CharField(max_length=256, null=True, blank=True)


class DriverToVehicle(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle', null=True, blank=True)