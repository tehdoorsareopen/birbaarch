import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class User(AbstractUser):
    system_id = models.UUIDField(default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.CASCADE)
