from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import CustomUser, Team

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id","email","username","team_id")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id","name","description")