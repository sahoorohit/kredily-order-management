from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return "{}".format(self.username)
