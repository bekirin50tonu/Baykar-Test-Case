from django.contrib import admin

from management.models import PlaneType, ItemType, ProducedItem, ProducedPlane, PlaneParticipant, PlaneRecipe


# Register your models here.
@admin.register(PlaneRecipe) # tanımlama dekoratörüdür. admin tablosuna tanımlar.
class PlaneRecipeAdmin(admin.ModelAdmin):
    list_display = ("id","get_plane_type","get_item_type","count") # gösterilecek sütunlar belirtilir.

    def get_plane_type(self, obj): # ilişkili veriler için tanımlama için kullanılır.
        return obj.plane_type.name
    get_plane_type.short_description = "Plate Type" # admin sayfasında sütun açıklamasını tanımlar.

    def get_item_type(self, obj):
        return obj.item_type.name
    get_item_type.short_description = "Item Type"


@admin.register(PlaneType)
class PlaneTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_plane_type", "get_team_name")

    def get_plane_type(self, obj):
        return obj.plane_type.name

    get_plane_type.short_description = "Plate Type"

    def get_team_name(self, obj):
        return obj.team.name

    get_team_name.short_description = "Team Name"


@admin.register(ProducedItem)
class ProducedItemAdmin(admin.ModelAdmin):
    list_display = ("get_item_name", "get_member_username","is_used")

    def get_item_name(self, obj):
        return obj.item.name

    get_item_name.short_description = "Item Name"

    def get_member_username(self, obj):
        return obj.member.username

    get_member_username.short_description = "Member Username"


@admin.register(ProducedPlane)
class ProducedPlaneAdmin(admin.ModelAdmin):
    list_display = ("id","get_plane_name")

    def get_plane_name(self, obj):
        return obj.plane_type.name

    get_plane_name.short_description = "Plane Name"


@admin.register(PlaneParticipant)
class PlaneParticipantAdmin(admin.ModelAdmin):
    list_display = ("id","get_plane_name", "get_item_name")

    def get_plane_name(self, obj):
        return obj.plane.plane_type.name

    get_plane_name.short_description = "Plane Name"

    def get_item_name(self, obj):
        return obj.part.item.name

    get_item_name.short_description = "Item Name"
