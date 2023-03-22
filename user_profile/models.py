from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=255)
    last_login = models.DateTimeField(null=True)
    last_request = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.username}'
