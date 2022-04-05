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
    latitude = models.FloatField()
    longitude = models.FloatField()
    slug = models.SlugField(max_length=40, unique=True)
    url = models.URLField()

    def __str__(self) -> str:
        return self.slug


class LabTest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    test_date = models.DateTimeField()
    location = models.ForeignKey(
        Location, on_delete=models.DO_NOTHING, to_field="slug")
    payment_date = models.DateTimeField(blank=True, null=True)
    result = models.BooleanField(blank=True, null=True)
    result_date = models.DateTimeField(blank=True, null=True)
    canceled = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)
    verify_id = models.UUIDField(
        default=uuid.uuid4, primary_key=False, unique=True)
