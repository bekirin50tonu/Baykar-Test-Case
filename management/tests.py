from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import CustomUser, Team
from management.models import ItemType, PlaneType, ProducedItem, PlaneRecipe


# Create your tests here.


class DataSetTestCase(APITestCase):
    username_montage = "productuser"
    username_product = "montageuser"
    password = "password"

    user_montage = None
    user_product = None

    montage_team = None
    product_team = None

    def setUp(self):
        # Kullanıcıları oluştur veya mevcut olanı al
        self.user_montage, _ = CustomUser.objects.get_or_create(
            username=self.username_montage,
            defaults={"email": "test1@example.com", "password": self.password}
        )
        self.user_product, _ = CustomUser.objects.get_or_create(
            username=self.username_product,
            defaults={"email": "test2@example.com", "password": self.password}
        )

        # Takımları oluştur veya mevcut olanı al
        self.montage_team, _ = Team.objects.get_or_create(
            name="Montaj",
            defaults={"description": "Montaj Team", "has_montage": True}
        )
        self.product_team, _ = Team.objects.get_or_create(
            name="Aviyonik",
            defaults={"description": "Aviyonik Team", "has_produce": True}
        )

        # Kullanıcılara takımları ata ve kaydet
        if self.user_montage.team != self.montage_team:
            self.user_montage.team = self.montage_team
            self.user_montage.save()

        if self.user_product.team != self.product_team:
            self.user_product.team = self.product_team
            self.user_product.save()

    # Üretilen parçaların geleceği dataset endpoint testleri

    ## Bilgiler doğruysa
    def test_get_produced_dataset(self):
        self.client.force_login(self.user_product)
        response = self.client.get(reverse('production-item-view-dataset'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Takım üretimden sorumlu değilse.
    def test_get_produced_dataset_with_forbidden_error(self):
        self.client.force_login(self.user_montage)
        response = self.client.get(reverse('production-item-view-dataset'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## Giriş yapılmamışsa.
    def test_get_produced_dataset_with_unauthorized_error(self):
        self.client.logout()
        self.assertFalse('_auth_user_id' in self.client.session)  # Kontrol et
        response = self.client.get(reverse('production-item-view-dataset'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Montaj takımı üretilen parçaların bilgileri dataset testleri.
    ## Bilgiler doğruysa
    def test_get_montage_dataset(self):
        self.client.force_login(self.user_montage)
        response = self.client.get(reverse('montage-plane-view-dataset'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Takım üretimden sorumlu değilse.
    def test_get_montage_dataset_with_forbidden_error(self):
        self.client.force_login(self.user_product)
        response = self.client.get(reverse('montage-plane-view-dataset'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## Giriş yapılmamışsa.
    def test_get_montage_dataset_with_unauthorized_error(self):
        self.client.logout()
        self.assertFalse('_auth_user_id' in self.client.session)  # Kontrol et
        response = self.client.get(reverse('montage-plane-view-dataset'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductItemsTestCase(APITestCase):
    username_montage = "productuser"
    username_product = "montageuser"
    password = "password"

    user_montage = None
    user_product = None

    montage_team = None
    product_team = None
    empty_team = None

    item_type = None

    def setUp(self):
        # Kullanıcıları oluştur veya mevcut olanı al
        self.user_montage, _ = CustomUser.objects.get_or_create(
            username=self.username_montage,
            defaults={"email": "test1@example.com", "password": self.password}
        )
        self.user_product, _ = CustomUser.objects.get_or_create(
            username=self.username_product,
            defaults={"email": "test2@example.com", "password": self.password}
        )

        # Takımları oluştur veya mevcut olanı al
        self.montage_team, _ = Team.objects.get_or_create(
            name="Montaj",
            defaults={"description": "Montaj Team", "has_montage": True}
        )
        self.product_team, _ = Team.objects.get_or_create(
            name="Aviyonik",
            defaults={"description": "Aviyonik Team", "has_produce": True}
        )
        self.empty_team, _ = Team.objects.get_or_create(
            name="Kanat",
            defaults={"description": "Kanat Team", "has_produce": True}
        )
        plane_type = PlaneType.objects.create(name="TB3", description="TB3 Type")
        self.item_type = ItemType.objects.create(name="TB3 Aviyonik Parça", plane_type=plane_type,
                                                 team=self.product_team)

        # Kullanıcılara takımları ata ve kaydet
        if self.user_montage.team != self.montage_team:
            self.user_montage.team = self.montage_team
            self.user_montage.save()

        if self.user_product.team != self.product_team:
            self.user_product.team = self.product_team
            self.user_product.save()

    # Üretilebilecek Parçalar Endpoint Testleri

    ## Bilgiler doğruysa.
    def test_get_item_types(self):
        self.client.force_login(self.user_product)
        response = self.client.get(reverse('production-item-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Eğer Montaj Takımı ise.
    def test_get_item_types_forbidden(self):
        self.client.force_login(self.user_montage)
        response = self.client.get(reverse('production-item-view'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## Eğer Kullanıcı giriş yapmamış ise.
    def test_get_item_types_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse('production-item-view'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ## Eğer obje eklenmişse.
    def test_post_produced_item(self):
        self.client.force_login(self.user_product)
        response = self.client.post(reverse('production-item-view'), {"item_type_id": self.item_type.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    ## Eğer item_type_id veriyi yok ise.
    def test_post_produced_item_bad_request(self):
        self.client.force_login(self.user_product)
        response = self.client.post(reverse('production-item-view'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ## Eğer montaj takımı erişmek isterse.
    def test_post_produced_item_forbidden(self):
        self.client.force_login(self.user_montage)
        response = self.client.post(reverse('production-item-view'), {"item_type_id": self.item_type.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## Eğer üretebileceği parça yok ise.
    def test_post_produced_item_not_found(self):
        self.client.force_login(self.user_montage)
        response = self.client.post(reverse('production-item-view'), {"item_type_id": self.item_type.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## Eğer giriş yapılmamış ise.
    def test_post_produced_item_unauthorized(self):
        self.client.logout()
        response = self.client.post(reverse('production-item-view'), {"item_type_id": self.item_type.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ## Eğer geri dönüşüm başarılı ise.
    def test_delete_produced_item(self):
        self.client.force_login(self.user_product)
        produced_item = ProducedItem.objects.get_or_create(item_id=self.item_type.id, member_id=self.user_product.id)[0]
        response = self.client.delete(reverse('production-item-view'), {"id": produced_item.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Eğer id verisi yok ise.
    def test_delete_produced_item_bad_request(self):
        self.client.force_login(self.user_product)
        response = self.client.delete(reverse('production-item-view'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ## Eğer id verisi veritabanında yok ise.
    def test_delete_produced_item_not_found(self):
        self.client.force_login(self.user_product)
        total = ProducedItem.objects.all().count() + 100
        response = self.client.delete(reverse('production-item-view'), {"id": total})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        ## Eğer montaj takımı istek atmış ise.

    def test_delete_produced_item_forbidden(self):
        self.client.force_login(self.user_montage)
        produced_item = ProducedItem.objects.get_or_create(item_id=self.item_type.id, member_id=self.user_product.id)[0]
        response = self.client.delete(reverse('production-item-view'), {"id": produced_item.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## Eğer montaj takımı istek atmış ise.
    def test_delete_produced_item_unauthorized(self):
        produced_item = ProducedItem.objects.get_or_create(item_id=self.item_type.id, member_id=self.user_product.id)[0]
        response = self.client.delete(reverse('production-item-view'), {"id": produced_item.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductPlaneTestCase(APITestCase):
    username_montage = "productuser"
    username_product = "montageuser"
    password = "password"

    user_montage = None
    user_product = None

    montage_team = None
    product_team = None
    empty_team = None

    def setUp(self):
        # Kullanıcıları oluştur veya mevcut olanı al
        self.user_montage, _ = CustomUser.objects.get_or_create(
            username=self.username_montage,
            defaults={"email": "test1@example.com", "password": self.password}
        )
        self.user_product, _ = CustomUser.objects.get_or_create(
            username=self.username_product,
            defaults={"email": "test2@example.com", "password": self.password}
        )

        # Takımları oluştur veya mevcut olanı al
        self.montage_team, _ = Team.objects.get_or_create(
            name="Montaj",
            defaults={"description": "Montaj Team", "has_montage": True}
        )
        self.product_team, _ = Team.objects.get_or_create(
            name="Aviyonik",
            defaults={"description": "Aviyonik Team", "has_produce": True}
        )
        self.empty_team, _ = Team.objects.get_or_create(
            name="Kanat",
            defaults={"description": "Kanat Team", "has_produce": True}
        )

        # Kullanıcılara takımları ata ve kaydet
        if self.user_montage.team != self.montage_team:
            self.user_montage.team = self.montage_team
            self.user_montage.save()

        if self.user_product.team != self.product_team:
            self.user_product.team = self.product_team
            self.user_product.save()

    ## Bilgiler doğruysa uçak tipleri gelir.
    def test_get_montage_planes(self):
        self.client.force_login(self.user_montage)
        response = self.client.get(reverse('production-plane-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Eğer kullanıcı üretim takımında ise giriş yapamaz.
    def test_get_montage_planes_forbidden(self):
        self.client.force_login(self.user_product)
        response = self.client.get(reverse('production-plane-view'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## Eğer kullanıcı yok ise.
    def test_get_montage_planes_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse('production-plane-view'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    ## Bilgiler doğruysa.
    def test_post_montage_planes(self):
        self.client.force_login(self.user_montage)

        # uçak tipi eklenir.
        plane_type,_ = PlaneType.objects.get_or_create(name="TB3", defaults={"description": "TB3 Type"})

        # gerekli üretim takımları eklemesi yapılır.
        team_list = [
            Team(name="Aviyonikk", description="Aviyonik Team", has_produce=True),
            Team(name="Kanatt", description="Kanat Team", has_produce=True),
            Team(name="Kuyrukk", description="Kuyruk Team", has_produce=True),
            Team(name="Gövdee", description="Gövde Team", has_produce=True),
        ]
        teams = Team.objects.bulk_create(team_list)

        # gerekli parça tipleri eklemesi yapılır. rol tabanlıdır ve o rol üretebilir.
        item_type_list = []
        for team in teams:
            item_type_list.append(ItemType(name=team.name, plane_type=plane_type, team_id=team.id))
        items = ItemType.objects.bulk_create(item_type_list)

        # uçağın gereken parça tarifi eklenir ve 1 fazlası olacak şekilde parça üretimi yaptırılır.
        produced_item = []
        plane_recipe_list = []
        for item in items:
            plane_recipe_list.append(PlaneRecipe(plane_type=item.plane_type, item_type=item, count=1))
            produced_item.append(ProducedItem(item=item, member=self.user_montage))
            produced_item.append(ProducedItem(item=item, member=self.user_montage))
        PlaneRecipe.objects.bulk_create(plane_recipe_list)
        ProducedItem.objects.bulk_create(produced_item)

        # gerekli veriler ile istek atılır.
        response = self.client.post(reverse('production-plane-view'), {"type": plane_type.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # eğer uçak tipi verilmemiş ise.
    def test_post_montage_planes_bad_request(self):
        self.client.force_login(self.user_montage)
        response = self.client.post(reverse('production-plane-view'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # eğer üretim takımında ise.
    def test_post_montage_planes_forbidden(self):
        self.client.force_login(self.user_product)
        response = self.client.post(reverse('production-plane-view'), {"type": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # eğer uçak tarifi yok ise.
    def test_post_montage_planes_not_found(self):
        self.client.force_login(self.user_montage)
        plane_type = PlaneType.objects.create(name="TB2", description="TB2 Type")

        response = self.client.post(reverse('production-plane-view'), {"type": plane_type.id})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # eğer uçak tarifi var ama parçalar yok ise.
    def test_post_montage_planes_unprocessable_entity(self):
        self.client.force_login(self.user_montage)
        ProducedItem.objects.all().delete()

        # uçak tipi eklenir.
        plane_type, _ = PlaneType.objects.get_or_create(name="TB3", defaults={"description": "TB3 Type"})

        # gerekli üretim takımları eklemesi yapılır.
        team_list = [
            Team(name="Aviyonikk", description="Aviyonik Team", has_produce=True),
            Team(name="Kanatt", description="Kanat Team", has_produce=True),
            Team(name="Kuyrukk", description="Kuyruk Team", has_produce=True),
            Team(name="Gövdee", description="Gövde Team", has_produce=True),
        ]
        teams = Team.objects.bulk_create(team_list)

        # gerekli parça tipleri eklemesi yapılır. rol tabanlıdır ve o rol üretebilir.
        item_type_list = []
        for team in teams:
            item_type_list.append(ItemType(name=team.name, plane_type=plane_type, team_id=team.id))
        items = ItemType.objects.bulk_create(item_type_list)

        # uçağın gereken parça tarifi eklenir ve 1 fazlası olacak şekilde parça üretimi yaptırılır.
        plane_recipe_list = []
        for item in items:
            plane_recipe_list.append(PlaneRecipe(plane_type=item.plane_type, item_type=item, count=1))
        PlaneRecipe.objects.bulk_create(plane_recipe_list)

        response = self.client.post(reverse('production-plane-view'), {"type": plane_type.id})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # eğer kişi giriş yapmamış ise.
    def test_post_montage_planes_unauthorized(self):
        self.client.logout()
        plane_type = PlaneType.objects.create(name="TB2", description="TB2 Type")

        response = self.client.post(reverse('production-plane-view'), {"type": plane_type.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PlaneTypeTestCase(APITestCase):
    username_montage = "productuser"
    username_product = "montageuser"
    password = "password"

    user_montage = None
    user_product = None

    montage_team = None
    product_team = None

    def setUp(self):
        # Kullanıcıları oluştur veya mevcut olanı al
        self.user_montage, _ = CustomUser.objects.get_or_create(
            username=self.username_montage,
            defaults={"email": "test1@example.com", "password": self.password}
        )
        self.user_product, _ = CustomUser.objects.get_or_create(
            username=self.username_product,
            defaults={"email": "test2@example.com", "password": self.password}
        )

        # Takımları oluştur veya mevcut olanı al
        self.montage_team, _ = Team.objects.get_or_create(
            name="Montaj",
            defaults={"description": "Montaj Team", "has_montage": True}
        )
        self.product_team, _ = Team.objects.get_or_create(
            name="Aviyonik",
            defaults={"description": "Aviyonik Team", "has_produce": True}
        )

        # Kullanıcılara takımları ata ve kaydet
        if self.user_montage.team != self.montage_team:
            self.user_montage.team = self.montage_team
            self.user_montage.save()

        if self.user_product.team != self.product_team:
            self.user_product.team = self.product_team
            self.user_product.save()

    ## Bilgiler doğruysa uçak tipleri gelir.
    def test_get_plane_types(self):
        self.client.force_login(self.user_montage)
        response = self.client.get(reverse('planes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Eğer kullanıcı üretim takımında ise.
    def test_get_plane_types_forbidden(self):
        self.client.force_login(self.user_product)
        response = self.client.get(reverse('planes'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    ## Eğer kullanıcı giriş yapmamış ise.
    def test_get_plane_types_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse('planes'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


