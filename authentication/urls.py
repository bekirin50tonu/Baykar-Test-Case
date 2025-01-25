from django.urls import path
from .views import LoginView, LogoutView, WhoAmIView

urlpatterns = [
    path("whoami/", WhoAmIView.as_view(), name="whoami"), # user bilgisi almak için tanımlanan endpoint.
    path('login/', LoginView.as_view(), name='login'), # giriş yapmak için kullanılan endpoint.
    path('logout/', LogoutView.as_view(), name='logout'), # çıkış yapmak için kullanılan endpoint.


]
