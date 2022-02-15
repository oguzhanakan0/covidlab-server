from unittest import result
from django.db import models
from src.enums import AuthSource, Relationship
from user.models import User
import uuid


class Location(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=12)
    email = models.EmailField()


class LabTest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    test_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    payment_date = models.DateField(blank=True, null=True)
    result = models.BooleanField(blank=True, null=True)
