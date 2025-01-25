from django.urls import path

from .views import login_page, dashboard_page, montage_page

urlpatterns = [
    path("dashboard", dashboard_page, name='dashboard-page'), # production sayfasını verir.
    path("montage", montage_page, name='montage-page'), # montaj sayfasını verir.
    path('', login_page, name='login-page'), # login sayfasını getirir.

]
