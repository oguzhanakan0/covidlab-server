from django.db import models
import uuid

from user.models import User
# Create your models here.


class Notif(models.Model):

    class NotifTypeOptions(models.TextChoices):
        primary = 'P'
        warning = 'W'
        danger = 'D'
        success = 'S'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=80)
    content = models.CharField(max_length=240)
    notif_type = models.CharField(
        max_length=2, choices=NotifTypeOptions.choices)
    date_read = models.DateTimeField(blank=True, null=True)
