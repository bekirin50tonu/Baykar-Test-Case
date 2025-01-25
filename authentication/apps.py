from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # veritabanı eklemelerinde id tanımlamasıdır.
    name = 'authentication' # giriş tanımlama ismini belirler.

