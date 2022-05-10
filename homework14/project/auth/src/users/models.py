import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    system_id = models.UUIDField(default=uuid.uuid4, editable=False)
