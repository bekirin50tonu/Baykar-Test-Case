from django.forms.models import model_to_dict
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers.serializers import  UserSerializer


# Gelen kullanıcı işlemlerinin yürütüleceği fonksiyonları içerir.
from django.contrib.auth import authenticate, login, logout

# Giriş sistemi tanımlanması.
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login with username and password endpoint.", ## endpoint açıklaması.
        request_body=openapi.Schema( ## form body için istenilen verileri içerir.
            type=openapi.TYPE_OBJECT, ## Obje olması gerekmektedir.
            required=["username", 'password'], ## mutlaka içermelidir. validation işlemleri olarak çalışır.
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD)
            },
        ),
        responses={ ## Örnek olarak verilen cevapları içerir.
            200: openapi.Response("Success!", examples={"application/json": {
  "message": "Login successful",
  "user": {
    "email": "test_user0@test.com",
    "first_name": "Kanat",
    "last_name": "Uyesi",
    "username": "user0",
    "team": {
      "id": 1,
      "name": "Kanat",
      "description": "Kanat Takımını Temsil Eder. Üretimden Sorumludur.",
      "has_produce": True,
      "has_montage": False
    },
    "is_staff": False,
    "is_superuser": False,
    "is_active": True
  }
}}),
            401: openapi.Response("Unauthentication!", examples={"application/json": {"error": "Invalid credentials"}})

        },
    )
    def post(self, request):
        ## credential için gereken verileri alır.
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password) ## django auth sistemi ile tanımlama sağlanır.

        if user:
            login(request, user) ## eğer kullanıcı var ise session işlemini başlatır.-
            serializer = UserSerializer(user)
            return Response({"message": "Login successful","user":serializer.data})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Çıkış sistemi tanımlanması.
class LogoutView(APIView):

    @swagger_auto_schema(
        operation_description="Logout your Session.",
        responses={
            200: openapi.Response("Success!", examples={"application/json": {"message": "Logout Succeed."}}),
            401: openapi.Response("Unauthenticated!",
                                  examples={"application/json": {"error": "Unauthenticated User. Please Log in."}})

        },
    )
    def get(self, request):

        if self.request.user.is_authenticated: ## çalışması için giriş yapmış olması gerekmektedir.
            logout(request) ## çıkış işlemini gerçekleştirir. site cookie içerisindeki sessionid bilgisini temizler.
            return Response({"message": "Logout Succeed."}, status=status.HTTP_200_OK)
        return Response({"error": "Unauthenticated User. Please Log in."}, status=status.HTTP_401_UNAUTHORIZED, )

# Kimlik bilgilerinin cevaplanması.
class WhoAmIView(APIView):

    @swagger_auto_schema(
        operation_description="Gives Your User Data.",
        responses={
            200: openapi.Response("Success!", examples={"application/json": {
                "user": {
                    "email": "example@example.com",
                    "first_name": "Alan",
                    "last_name": "Tuning",
                    "username": "testuser",
                    "team": {
                        "id": 1,
                        "name": "Kanat Takımı",
                        "description": "Kanat Yapımından Sorumlu."
                    },
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True
                }}}),
            401: openapi.Response("Unauthenticated!",
                                  examples={"application/json": {"error": "Invalid credentials"}})

        },
    )
    def get(self, request):

        user = self.request.user
        serializer = UserSerializer(user) ## aldığımız modeli response için uygun hale getirmek için kullanılır.
        ## istenilen veriler girilir. password gibi gereksiz veriler gönderilmez.

        ## geçerli kullanıcı ise bilgiler gönderilir.
        if user.is_authenticated:
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        ## geçersiz ise hata mesajı gönderilir.
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
