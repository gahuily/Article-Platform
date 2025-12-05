from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    interest_keywords = models.TextField(blank=True, default="", help_text="관심 분야 (쉼표 구분) 저장. 규칙 기반 큐레이션 근거")

    def __str__(self):
        return self.username