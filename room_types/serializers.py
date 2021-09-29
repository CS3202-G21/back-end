from rest_framework import serializers
from .models import RoomType


# Room Type Serializer
class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'