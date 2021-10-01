from django.urls import path, include
from .api import RoomReservationViewSet, RoomReservationSuccessViewSet, RoomCheckInViewSet, RoomCheckOutViewSet, AddRoomReviewViewSet, GetTodayRoomReservationsViewSet, GetRoomReviewsViewSet

urlpatterns = [
    path('api/room_reservations', RoomReservationViewSet.as_view()),
    path('api/room_reservations/payment_success', RoomReservationSuccessViewSet.as_view()),
    path('api/room_reservations/check_in', RoomCheckInViewSet.as_view()),
    path('api/room_reservations/check_out', RoomCheckOutViewSet.as_view()),
    path('api/room_reservations/add_review', AddRoomReviewViewSet.as_view()),
    path('api/room_reservations/today_reservations', GetTodayRoomReservationsViewSet.as_view()),
    path('api/room_reservations/get_reviews', GetRoomReviewsViewSet.as_view()),
]