import uuid
import random

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    system_id = models.UUIDField(default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=256)


class Task(models.Model):
    name = models.CharField(max_length=256)
    system_id = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.TextField()
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_by')
    assigned_on = models.ForeignKey('User', on_delete=models.CASCADE, related_name='assigned_on')
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.assigned_on = self.get_random_user_to_assign()
        super().save(*args, **kwargs)

    # Custom methods

    def get_random_user_to_assign(self):
        return random.choice(list(User.objects.all()))
