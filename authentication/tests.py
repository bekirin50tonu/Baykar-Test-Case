from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import CustomUser


# Create your tests here.


class LoginTestCase(APITestCase):

    username = "superuser"
    password = "password"

    user = None

    def setUp(self):
        ## eğer kullanıcı yoksa veritabanına eklemesi gerekmektedir.
        try:
            self.user = CustomUser.objects.get(username="superuser")
        except CustomUser.DoesNotExist:
            self.user = CustomUser.objects.create_user(self.username, "test@example.com",
                                                 self.password)  ## kullanıcı yaratma işlemi.

    def test_login(self): ## giriş sistemi testi.
        response = self.client.post(reverse('login'), data={'username': self.username, 'password': self.password}) # giriş yapacağı endpointe credential verilerini gönderir.
        self.assertEqual(response.status_code, status.HTTP_200_OK) # sorgu geçerliyse testi geçer.

    def test_whoami(self): ## kullanıcı bilgileri testi.
        self.client.force_login(self.user) # veritabanından aldığı kullanıcıyla giriş yaptırır.
        response = self.client.get(reverse('whoami')) # bilgi alabileceği endpointi sistemden alır ve sorgu yapar.
        print(response.data) # Gelen bilgiyi görmek için konsola bastırır.
        self.assertEqual(response.status_code, status.HTTP_200_OK) # sorgu geçerliyse testi geçer.

    def test_logout(self): ## kullanıcı çıkış testi.
        self.client.force_login(self.user) # veritabanından aldığı kullanıcıyla giriş yaptırır.
        response = self.client.get(reverse('logout')) # çıkış yapacağı endpointe sorgu gönderir.
        self.assertEqual(response.status_code, status.HTTP_200_OK) # sorgu geçerliyse testi geçer.
