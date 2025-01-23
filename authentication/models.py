import secrets
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    team = models.OneToOneField(Team, on_delete=models.CASCADE, blank=True, null=True)
