from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import CustomUser, Team

# Admin arayüzü kullanıcı ayarları
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'team')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}), #olması gereken tanımları içeriyor. Kendisi standartta olan tanımlar.
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',), # ön yüzdeki sınıfını belirtir.
            'fields': ('username', 'email', 'password1', 'password2', 'team'), #ilk sekmesinde yer alan verileri belirtir.
        }), # Takım belirtmek için bu ayarın eklenmesi gerekiyor.
    )
    list_display = ('username', 'email', 'team', 'is_staff', 'is_active')  # Liste görünümündeki alanlar
    search_fields = ('username', 'email')  # Arama yapılacak alanlar
    ordering = ('username',) # Datatable sıralamasının kuralını belirler.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id","name","description","has_produce","has_montage") # modeldeki hangi verilerin görüneceğini belirler.