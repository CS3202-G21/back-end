from .models import RoomType
from rest_framework import viewsets, permissions
from .serializers import RoomTypeSerializer


# Room Type ViewSet
class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RoomTypeSerializer
