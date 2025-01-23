from django.urls import path

from .views import login_page, dashboard_page

urlpatterns = [
    path("dashboard", dashboard_page, name='dashboard-page'),
    path('', login_page, name='login-page'),

]
