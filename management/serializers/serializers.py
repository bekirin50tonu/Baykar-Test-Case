from rest_framework import serializers

from authentication.serializers.serializers import UserSerializer, TeamSerializer
from management.models import ProducedItem, ItemType, PlaneType, PlaneParticipant, ProducedPlane


class PlaneTypeSerializer(serializers.ModelSerializer): # Uçak tipi için model dönüştürme işlemini sağlar
    class Meta: #meta data tanımlaması
        model = PlaneType # modeli tanımlar
        fields = '__all__' # hangi verilerin verilmesi gerektiğini belirtir.

class ItemTypeSerializer(serializers.ModelSerializer):
    plane_type = PlaneTypeSerializer() # içerisinde yer alan verinin bir diğer serializer ile dönüşümü ve karşıya istenilen şekilde iletilmesini sağlar.
    team = TeamSerializer()
    class Meta:
        model = ItemType
        fields = '__all__'


class ProductItemSerializer(serializers.ModelSerializer):
    item = ItemTypeSerializer()
    member = UserSerializer()

    class Meta:
        model = ProducedItem
        fields = '__all__'

class ProductPlaneSerializer(serializers.ModelSerializer):
    plane_type = PlaneTypeSerializer()
    member = UserSerializer()

    class Meta:
        model = ProducedPlane
        fields = '__all__'

class PlaneParticipantSerializer(serializers.ModelSerializer):
    plane = ProductPlaneSerializer()
    part = ProductItemSerializer()
    class Meta:
        model = PlaneParticipant
        fields = '__all__'
