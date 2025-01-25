#!/bin/bash

# Veritabanı sıfırlama işlemini gerçekleştirir.
python manage.py flush --no-input

# Veritabanı için eklenmesi, düzeltilmesi ve silinmesi gereken tabloları bu kod yardımıyla oluşturur.
python manage.py makemigrations

# Veritabanı için oluşturulan python kodlarını bu kod yardımıyla veritabanına yapılması gereken işlemleri yapılır.
python manage.py migrate

# Uygulama başlamadan önce endpoint testleri gerçekleştirilir.
python manage.py test

# Uygulama için gereken verileri bu kod yardımıyla eklemesi yapılır.
python manage.py seed_database

# Sunucuyu çalıştırır.
python manage.py runserver 0.0.0.0:8000