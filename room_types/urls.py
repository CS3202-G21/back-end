from rest_framework import routers
from .api import RoomTypeViewSet

router = routers.DefaultRouter()
router.register('api/room_types', RoomTypeViewSet, 'room_types')

urlpatterns = router.urls
