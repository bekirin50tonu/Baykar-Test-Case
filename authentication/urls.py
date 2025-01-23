from django.urls import path
from .views import TeamView, LoginView, LogoutView, WhoAmIView

urlpatterns = [
    path("auth/whoami/", WhoAmIView.as_view(), name="whoami"),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('teams/', TeamView.as_view(), name='team-list'),


]
