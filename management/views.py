from http import HTTPStatus

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Team
from .middlewares import isMontageTeam, isProductTeam

from management.models import ProducedItem, ItemType, PlaneType, PlaneParticipant, PlaneRecipe, ProducedPlane
from management.serializers.serializers import ProductItemSerializer, PlaneTypeSerializer, ProductPlaneSerializer, \
    PlaneParticipantSerializer


class PlaneViewApi(APIView):
    @swagger_auto_schema(
        operation_description="Get Plane Types.",  ## endpoint açıklaması.
        responses={  ## Örnek olarak verilen cevapları içerir.
            200: openapi.Response("Success!", examples={"application/json": {
                "planes": [
                    {
                        "id": 1,
                        "name": "TB3",
                        "description": "TB3 IHA"
                    },
                    {
                        "id": 2,
                        "name": "TB2",
                        "description": "Tb2 IHA"
                    },
                    {
                        "id": 3,
                        "name": "AKINCI",
                        "description": "Akıncı IHA"
                    },
                    {
                        "id": 4,
                        "name": "KIZILELMA",
                        "description": "Kızılelma IHA"
                    }
                ]

            }}),
            401: openapi.Response("Unauthentication!", examples={"application/json": {"error": "Invalid credentials"}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),

        },
    )
    @isMontageTeam
    def get(self, request):
        # veritabanından iha tiplerini alır ve json tipine dönüşümünü sağlar.
        planes = PlaneType.objects.all()
        serializer = PlaneTypeSerializer(planes, many=True)

        return Response({"planes": serializer.data})


class ProductionItemApi(APIView):

    @swagger_auto_schema(
        operation_description="Get Produced Items..",  ## endpoint açıklaması.
        responses={  ## Örnek olarak verilen cevapları içerir.
            200: openapi.Response("Success!", examples={"application/json": {"data": [
                {
                    "id": 5,
                    "name": "TB3 Aviyonik Takımı",
                    "plane_type_id": 1,
                    "team_id": 4
                },
                {
                    "id": 11,
                    "name": "TB2 Aviyonik Takımı",
                    "plane_type_id": 2,
                    "team_id": 4
                },
                {
                    "id": 14,
                    "name": "KIZILELMA Aviyonik Takımı",
                    "plane_type_id": 4,
                    "team_id": 4
                },
                {
                    "id": 17,
                    "name": "Akıncı Aviyonik Takımı",
                    "plane_type_id": 3,
                    "team_id": 4
                }
            ]}}),
            401: openapi.Response("Unauthentication!", examples={"application/json": {"error": "Invalid credentials"}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),
        },
    )
    @isProductTeam
    def get(self, request):

        # kullanıcının takımına göre üretim izni olan parça tiplerini alır.
        item_types = ItemType.objects.filter(team=request.user.team).values()
        return Response({"data": item_types})

    @swagger_auto_schema(
        operation_description="Product Item with Item Id.",  ## endpoint açıklaması.
        request_body=openapi.Schema(  ## form body için istenilen verileri içerir.
            type=openapi.TYPE_OBJECT,  ## Obje olması gerekmektedir.
            required=["item_type_id"],  ## mutlaka içermelidir. validation işlemleri olarak çalışır.
            properties={
                'item_type_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={  ## Örnek olarak verilen cevapları içerir.
            201: openapi.Response("Success!", examples={"application/json": {"message": "Product Created."}}),
            400: openapi.Response("Bad Request!", examples={"application/json": {"error": "item_type_id is required"}}),
            401: openapi.Response("Unauthentication!", examples={"application/json": {"error": "Invalid credentials"}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),
            404: openapi.Response("Not Found", examples={
                "application/json": {"error": f"Your Team's not produce any part of item."}}),
        },
    )
    @isProductTeam
    def post(self, request):
        # id verisini alır, eğer yoksa 400 Bad Request hatası döndürür.
        id = request.data.get("item_type_id")
        if id is None:
            return Response({"error": "item_type_id is required"}, 400)
        # gönderilen parça tipine göre ve takım bilgisine göre sorgu atar. eğer yoksa 404 Not Found döndürür.
        item_type = ItemType.objects.filter(id=id, team=self.request.user.team).first()
        if not item_type:
            return Response({"error": f"Your Team's not produce any part of item."}, status=HTTPStatus.NOT_FOUND)

        # parçalar üretilenlerin tablosuna eklenir. parça tipiyle ve kişinin kendisiyle birlikte ekleme yapar.
        ProducedItem.objects.create(item=item_type, member=self.request.user)
        return Response({"message": "Product Created."}, HTTPStatus.CREATED)

    @swagger_auto_schema(
        operation_description="Recycle Item with Produced Item Id.",  ## endpoint açıklaması.
        request_body=openapi.Schema(  ## form body için istenilen verileri içerir.
            type=openapi.TYPE_OBJECT,  ## Obje olması gerekmektedir.
            required=["id"],  ## mutlaka içermelidir. validation işlemleri olarak çalışır.
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={  ## Örnek olarak verilen cevapları içerir.
            200: openapi.Response("Success!", examples={"application/json": {"message": "Item Recycled."}}),
            400: openapi.Response("Bad Request!", examples={"application/json": {"error": "id is required"}}),
            404: openapi.Response("Not Found!", examples={"application/json": {"message": "Item Not Found."}}),
            401: openapi.Response("Unauthentication!", examples={"application/json": {"error": "Invalid credentials"}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),
        },
    )
    @isProductTeam
    def delete(self, request):
        # id verisini alır, eğer yoksa 400 Bad Request hatası döndürür.
        id = request.data.get("id")
        if id is None:
            return Response({"error": "id is required"}, HTTPStatus.BAD_REQUEST)

        # id verisine göre bulunur. yoksa 404 Not Found ile geri döndürülür.
        item = ProducedItem.objects.filter(id=id).first()
        if not item:
            return Response({"message": "Item Not Found."},HTTPStatus.NOT_FOUND)
        # Silinme işlemi gerçekleşir.
        item.delete()
        return Response({"message": "Item Recycled."},HTTPStatus.OK)


# Server-side datatable model ve sütun tanımlamalarını içerir.
class ProductionItemViewDataset(viewsets.ModelViewSet):
    serializer_class = ProductItemSerializer  # Modelin ilişkileriyle birlikte json olarak dönüşümünü sağlarç.
    filter_backends = [SearchFilter]  # Arama filtresi tanımlamasını içerir.
    search_fields = ['item_name']  # hangi sütuna göre arama yapabileceğini belirler.

    def get_queryset(self):
        # kişinin hangi takımda olduğunu ve o takıma göre parça tiplerinin veritabanından alınmasını sağlar.
        user = self.request.user
        item_types = ItemType.objects.filter(team=user.team).all()

        # üretilen parçaları listelemek için bir takımın üretebileceği parça tipleri ile bir liste yapılır.
        item_list = [x.id for x in item_types]
        # Liste içerisinde yer alan parça id bilgileri ile istenen veriler alınır.
        return ProducedItem.objects.filter(item_id__in=item_list).all().order_by("id")

    @swagger_auto_schema(
        operation_description="Get a list of production items for the user's team.",
        responses={
            200: openapi.Response(
                "Success!",
                examples={"application/json": {
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 10,
                            "item": {
                                "id": 5,
                                "plane_type": {
                                    "id": 1,
                                    "name": "TB3",
                                    "description": "TB3 IHA"
                                },
                                "team": {
                                    "id": 4,
                                    "name": "Aviyonik Takımı",
                                    "description": "Elektronik Ekipmanlar yapar."
                                },
                                "name": "TB3 Aviyonik Takımı"
                            },
                            "member": {
                                "email": "bgrmz@yandex.com",
                                "first_name": "Bekir",
                                "last_name": "Görmez",
                                "username": "bekirin50tonu",
                                "team": {
                                    "id": 4,
                                    "name": "Aviyonik Takımı",
                                    "description": "Elektronik Ekipmanlar yapar."
                                },
                                "is_staff": True,
                                "is_superuser": True,
                                "is_active": True
                            },
                            "is_used": True
                        },
                    ]
                }}
            ),
            401: openapi.Response("Unauthorized!", examples={"application/json": {"error": "Unauthorized."}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),
        },
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search for items by name.",
                type=openapi.TYPE_STRING
            )
        ],
    )
    @isProductTeam
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Uçak montaj tanımlamalarını içerir.
class ProductionPlaneView(APIView):
    @swagger_auto_schema(
        operation_description="Get all Plane Participant objects.",  ## endpoint açıklaması.
        responses={  ## Örnek olarak verilen cevapları içerir.
            200: openapi.Response("Success!", examples={"application/json": {"data": [
                {
                    "id": 25,
                    "plane": {
                        "id": 8,
                        "plane_type": {
                            "id": 1,
                            "name": "TB3",
                            "description": "TB3 IHA"
                        },
                        "member": {
                            "email": "bgrmz@yandex.com",
                            "first_name": "Bekir",
                            "last_name": "Görmez",
                            "username": "bekirin50tonu",
                            "team": {
                                "id": 5,
                                "name": "Montaj Takımı",
                                "description": "Parçalarla Montaj Yapar."
                            },
                            "is_staff": True,
                            "is_superuser": True,
                            "is_active": True
                        }
                    },
                    "part": {
                        "id": 1,
                        "item": {
                            "id": 2,
                            "plane_type": {
                                "id": 1,
                                "name": "TB3",
                                "description": "TB3 IHA"
                            },
                            "team": {
                                "id": 1,
                                "name": "Kanat Takımı",
                                "description": "Kanat Yapımından Sorumlu."
                            },
                            "name": "TB3 Kanat Takımı"
                        },
                        "member": {
                            "email": "bgrmz@yandex.com",
                            "first_name": "Bekir",
                            "last_name": "Görmez",
                            "username": "bekirin50tonu",
                            "team": {
                                "id": 5,
                                "name": "Montaj Takımı",
                                "description": "Parçalarla Montaj Yapar."
                            },
                            "is_staff": True,
                            "is_superuser": True,
                            "is_active": True
                        },
                        "is_used": True
                    }
                }
            ]}}),
            401: openapi.Response("Unauthentication!", examples={"application/json": {"error": "Invalid credentials"}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),
        },
    )
    @isMontageTeam
    def get(self, request):
        # Üretilen uçağın parçalarını gösterilmesini sağlar.
        data = PlaneParticipant.objects.all()
        serializer = PlaneParticipantSerializer(data, many=True)
        return Response({"data": serializer.data})

    @swagger_auto_schema(
        operation_description="Montage Plane endpoint.",  ## endpoint açıklaması.
        request_body=openapi.Schema(  ## form body için istenilen verileri içerir.
            type=openapi.TYPE_OBJECT,  ## Obje olması gerekmektedir.
            required=["id"],  ## mutlaka içermelidir. validation işlemleri olarak çalışır.
            properties={
                'type': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={  ## Örnek olarak verilen cevapları içerir.
            200: openapi.Response("Success!", examples={"application/json": {"message": "Product Created."}}),
            400: openapi.Response("Bad Request!",
                                  examples={"application/json": {"error": "plane_type_id is required"}}),
            401: openapi.Response("Unauthentication!", examples={"application/json": {"error": "Invalid credentials"}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),
            404: openapi.Response("Not Found!",
                                  examples={"application/json": {"error": "Gereken Parça Listesi Bulunamadı."}}),
            422: openapi.Response("Unprocessable Entity!", examples={"application/json": {"errors": [
                {
                    "plane": "TB3",
                    "item": "TB3 Kanat Takımı",
                    "total": 2,
                    "count": 0
                },
                {
                    "plane": "TB3",
                    "item": "TB3 Gövde Takımı",
                    "total": 1,
                    "count": 0
                },
                {
                    "plane": "TB3",
                    "item": "TB3 Kuyruk Takımı",
                    "total": 3,
                    "count": 0
                },
                {
                    "plane": "TB3",
                    "item": "TB3 Aviyonik Takımı",
                    "total": 5,
                    "count": 1
                }
            ]}}),

        },
    )
    @isMontageTeam
    def post(self, request):
        # iha tipinin id bilgisi alınır ve iha üretim listesi alınması sağlanır.
        plane_type_id = request.data.get("type")
        if not plane_type_id:
            return Response({"error": "plane_type_id is required"}, 400)

        plane_recipe = PlaneRecipe.objects.filter(plane_type_id=plane_type_id).all()

        # eğer parça tarifi yoksa 404 Not Found hatası döndürülür.
        if not plane_recipe:
            return Response({"error": "Gereken Parça Listesi Bulunamadı."}, 404)

        # hata bilgilerini içerecek liste.
        stock_error = []
        # geçerli olan üretilen parça listesi.
        available_items = []

        # uçağın tarifine göre her bir tarifi döngüye alınır ve block olarak verilir. PlaneRecipe modeli olarak gelir.
        for block in plane_recipe:
            # veritabanı sorgusu yapılır. Recipe modelinden parça tipi ile o parçanın kullanılmamış olması gerekmektedir.
            produced_items = ProducedItem.objects.filter(item=block.item_type, is_used=False).all()

            # verilerin okunaklı ve erişilebilir olması için dictionary verisi.
            data = {
                "plane": block.plane_type.name,
                "item": block.item_type.name,
                "total": block.count,
                "count": produced_items.count(),
            }

            # eğer parça sayısı, olması gerekenden az ise data verisi hata mesajı listesine eklenir.
            if data["count"] < data["total"]:
                stock_error.append(data)
            # eğer sorun yoksa, ihtiyaç kadar parça listeden alınır ve kullanılacak parçaların listesine eklenir.
            else:
                available = list(produced_items[:data["count"]])
                available_items.extend(available)
        # eğer stokta bir tane bile problem varsa 400 Bad Request hatası vererek gerekli olan parça verileri döndürür.
        if len(stock_error) > 0:
            return Response({"errors": stock_error}, 422)

        # bir iha şeması hazırlanır. kullanılacak olan parçalar uçak tipi ile uçağın parçalarının yer aldığı tabloya eklenmesi sağlanır.
        produced_plane = ProducedPlane.objects.create(plane_type_id=plane_type_id, member_id=request.user.id)
        entry = [PlaneParticipant(plane=produced_plane, part=item) for item in available_items]
        PlaneParticipant.objects.bulk_create(
            entry)  # bulk create ile toplu ekleme sağlanır. büyük veri eklemesinde faydalı bir yöntemdir.

        # kullanılan verileri işaretlenmesi yapılır ve veritabanına kaydedilmesi sağlanır.
        for item in available_items:
            item.is_used = True
        ProducedItem.objects.bulk_update(available_items, fields=["is_used"])

        return Response({"message": "Product Created."})


# uçak için kullanılan parçaların datatable olarak gönderilmesi sağlanır.
class ProductionPlaneViewDataset(viewsets.ModelViewSet):
    model = PlaneParticipant  # modeli belirtir.
    queryset = PlaneParticipant.objects.all().order_by("id")  # veritabanından alınan verileri tutar.
    serializer_class = PlaneParticipantSerializer  # dönüştürücüyü tanımlar.



    @swagger_auto_schema(
        operation_description="Get a list of production items for the user's team.",
        responses={
            200: openapi.Response(
                "Success!",
                examples={"application/json": {
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 25,
                            "plane": {
                                "id": 8,
                                "plane_type": {
                                    "id": 1,
                                    "name": "TB3",
                                    "description": "TB3 IHA"
                                },
                                "member": {
                                    "email": "bgrmz@yandex.com",
                                    "first_name": "Bekir",
                                    "last_name": "Görmez",
                                    "username": "bekirin50tonu",
                                    "team": {
                                        "id": 5,
                                        "name": "Montaj Takımı",
                                        "description": "Parçalarla Montaj Yapar."
                                    },
                                    "is_staff": True,
                                    "is_superuser": True,
                                    "is_active": True
                                }
                            },
                            "part": {
                                "id": 1,
                                "item": {
                                    "id": 2,
                                    "plane_type": {
                                        "id": 1,
                                        "name": "TB3",
                                        "description": "TB3 IHA"
                                    },
                                    "team": {
                                        "id": 1,
                                        "name": "Kanat Takımı",
                                        "description": "Kanat Yapımından Sorumlu."
                                    },
                                    "name": "TB3 Kanat Takımı"
                                },
                                "member": {
                                    "email": "bgrmz@yandex.com",
                                    "first_name": "Bekir",
                                    "last_name": "Görmez",
                                    "username": "bekirin50tonu",
                                    "team": {
                                        "id": 5,
                                        "name": "Montaj Takımı",
                                        "description": "Parçalarla Montaj Yapar."
                                    },
                                    "is_staff": True,
                                    "is_superuser": True,
                                    "is_active": True
                                },
                                "is_used": True
                            }
                        }
                    ]
                }}
            ),
            401: openapi.Response("Unauthorized!", examples={"application/json": {"error": "Unauthorized."}}),
            403: openapi.Response("Forbitten", examples={"application/json": {"error": "Forbidden"}}),
        },
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search for items by name.",
                type=openapi.TYPE_STRING
            )
        ],
    )
    @isMontageTeam
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
