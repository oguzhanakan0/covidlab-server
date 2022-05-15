from django.db import models
from src.enums import AuthSource, Relationship
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser, ):

    REQUIRED_FIELDS = ('first_name', 'last_name')
    USERNAME_FIELD = 'email'
    is_authenticated = True

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)  # ok
    uid = models.CharField(max_length=100, unique=True)  # ok
    # username = models.CharField(
    #     max_length=40, unique=True, null=True, blank=True)  # ok
    first_name = models.CharField(max_length=100)  # ok
    last_name = models.CharField(max_length=100)  # ok
    email = models.EmailField(unique=True)  # ok
    last_login = models.DateTimeField(null=True, blank=True)  # ok
    first_joined = models.DateTimeField(null=True, blank=True)  # ok
    birth_date = models.DateField(blank=True, null=True)  # ok
    auth_source = models.CharField(
        max_length=20, choices=AuthSource.choices)  # ok
    is_info_complete = models.BooleanField(default=False)  # ok
    marketing_check = models.BooleanField(default=False)  # ok
    # is_anonymous = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
