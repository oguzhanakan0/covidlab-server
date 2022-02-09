from django.db import models
from django.db.models.base import Model
import uuid

# Create your models here.

# class Version(models.Model):
#     id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     version         = models.CharField(max_length=100,unique=True)
#     update_required = models.BooleanField(default=True)
#     release_date    = models.DateField(auto_now=True)
#     notes           = models.TextField()
#     is_latest       = models.BooleanField(default=True)

#     def __str__(self) -> str:
#         return self.version
    
#     @property
#     def version_int (self):
#         return int(self.version.replace('.',''))