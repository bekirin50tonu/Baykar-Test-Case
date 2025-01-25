from django.contrib.auth.models import AbstractUser
from django.db import models


# Takım Modeli Tanımlaması
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    has_produce = models.BooleanField(default=False)
    has_montage = models.BooleanField(default=False)

    #admin sayfasında görünmesini istediğimiz şekli verir. yoksa object olacak şekilde gösterir.
    def __str__(self):
        return self.name


# Sistem üzerine custom user sistemi tanımlamasıdır. Ekstra olarak takım eklemesi yapılmıştır.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
