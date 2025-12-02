from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    wallet = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username