import random

from django.core.management.base import BaseCommand

from authentication.models import Team, CustomUser
from management.models import PlaneType, ItemType, PlaneRecipe


class Command(BaseCommand):
    help = "Seed Team table with initial data."

    def handle(self, *args, **kwargs):

        superuser = CustomUser.objects.create_superuser(username='admin', email='admin@admin.com', password='password')

        # Takım listesi Oluşturma ve yaratma.
        list_team = [
            Team(name="Kanat", description="Kanat Takımını Temsil Eder. Üretimden Sorumludur.",
                 has_produce=True),
            Team(name="Gövde", description="Gövde Takımını Temsil Eder. Üretimden Sorumludur.",
                 has_produce=True),
            Team(name="Kuyruk", description="Kuyruk Takımını Temsil Eder. Üretimden Sorumludur.",
                 has_produce=True),
            Team(name="Aviyonik", description="Aviyonik Takımını Temsil Eder. Üretimden Sorumludur.",
                 has_produce=True),
            Team(name="Montaj", description="Montaj Takımını Temsil Eder. Üretimden Sorumludur.",
                 has_montage=True),
            Team(name="Admin", description="Bütün Takımları Yönetir.", has_produce=True, has_montage=True),
        ]
        teams = Team.objects.bulk_create(list_team)
        self.stdout.write(self.style.SUCCESS('Team Seeding completed successfully!'))

        # IHA tiplerini oluşturma ve yaratma.
        plane_type = [
            PlaneType(name="TB2", description="TB2 IHA"),
            PlaneType(name="TB3", description="TB3 IHA"),
            PlaneType(name="AKINCI", description="Akıncı IHA"),
            PlaneType(name="KIZILELMA", description="Kızılelma IHA"),
        ]
        plane_types = PlaneType.objects.bulk_create(plane_type)
        self.stdout.write(self.style.SUCCESS('Plane Types completed successfully!'))

        # Parça tipleri ve kullanıcıları yaratma
        item_type_list = []
        user_list = []
        for i, team in enumerate(teams):

            if team.has_produce and team.has_montage:
                superuser.team = team
                superuser.save()
                continue
            set_user = CustomUser(username=f"user{i}", team=team, first_name=f"{team.name}",
                                  last_name="Uyesi", email=f"test_user{i}@test.com")
            set_user.set_password('password')
            user_list.append(set_user)
            if team.has_produce:
                for plane_type in plane_types:
                    item_type_list.append(
                        ItemType(name=f"{plane_type.name}-{team.name}-Parçası", plane_type=plane_type, team=team))
        items = ItemType.objects.bulk_create(item_type_list)
        CustomUser.objects.bulk_create(user_list)
        self.stdout.write(self.style.SUCCESS('Item Types and Custom Users completed successfully!'))

        # IHA üretim tarifi yaratma.
        plane_recipe_list = []
        for plane_type in plane_types:
            for item in items:
                if item.plane_type.id == plane_type.id:
                    count = random.randint(1, 5)
                    plane_recipe_list.append(PlaneRecipe(plane_type=plane_type, item_type=item, count=count))
        PlaneRecipe.objects.bulk_create(plane_recipe_list)
        self.stdout.write(self.style.SUCCESS('Plane Recipe completed successfully!'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
