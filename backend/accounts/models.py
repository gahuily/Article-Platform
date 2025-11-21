from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    interests = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.username