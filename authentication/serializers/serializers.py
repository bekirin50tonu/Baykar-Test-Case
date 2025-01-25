from rest_framework import serializers

from authentication.models import CustomUser, Team


class TeamSerializer(serializers.ModelSerializer): # Takım Dönüştürücüsü
    class Meta:
        model = Team # istenilen model belirtilir.
        fields = ['id', 'name', 'description',"has_produce","has_montage"] # sorguda içermesi gereken başlıklar verilir.


class UserSerializer(serializers.ModelSerializer): ## Kullanıcı Dönüştürücüsü
    team = TeamSerializer(read_only=True) # Sorguda team id vermek yerine içermesi gereken verileri içermesini sağlar.

    class Meta:
        model = CustomUser # istenilen model belirtilir.
        fields = ["email","first_name","last_name","username","team","is_staff","is_superuser","is_active"] # içermesi istenen başlıklar verilir.
