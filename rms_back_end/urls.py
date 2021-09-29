from django.contrib import admin
from django.urls import path, include
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('rooms.urls')),
    path('', include('room_types.urls')),
    path('', include('restaurants.urls')),
    path('', include('menu_items.urls')),
    path('', include('special_offers.urls')),
    path('', include('customers.urls')),
    path('', include('staff.urls')),
    path('', include('room_reservations.urls')),
    path('', include('table_reservations.urls')),
    path('', include('customer_orders.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
