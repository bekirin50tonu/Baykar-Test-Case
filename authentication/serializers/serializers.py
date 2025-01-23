from rest_framework import serializers

from authentication.models import CustomUser, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']


class UserSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["email","first_name","last_name","username","team","is_staff","is_superuser","is_active"]
