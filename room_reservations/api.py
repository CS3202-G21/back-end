from .models import RoomReservation
from rooms.models import Room
from room_types.models import RoomType
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RoomReservationSerializer
from datetime import datetime, date
from rest_framework import serializers
from middleware.user_group_validation import is_customer, is_staff


# Room Reservation ViewSet
class RoomReservationViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RoomReservationSerializer

    def get(self, request):
        if not is_customer(request.user):
            raise serializers.ValidationError("Access Denied: You are not a customer")

        room_reservations_objs = RoomReservation.objects.filter(customer=request.user.id)
        room_reservations = []

        for obj in room_reservations_objs:
            reservation = obj.__dict__
            reservation.pop('_state')
            reservation['total_price'] = float(str(reservation['total_price']))
            room_reservations.append(reservation)

        return Response({"room_reservations": room_reservations})

    def post(self, request, *args, **kwargs):
        if not is_customer(request.user):
            raise serializers.ValidationError("Access Denied: You are not a customer")

        data = request.data
        data['customer'] = request.user.id
        data['total_price'], start_date, end_date = get_total_price(data)

        if are_dates_booked(start_date, end_date, data['room']):
            raise serializers.ValidationError("Given Dates are Booked")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        room_reservation = serializer.save()

        return Response({
            "room_reservation": RoomReservationSerializer(room_reservation, context=self.get_serializer_context()).data
        })


# View Set to update payment success
class RoomReservationSuccessViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RoomReservationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        reservation_id = data['reservation_id']

        try:
            reservation = RoomReservation.objects.get(id=reservation_id, customer=request.user.id)
        except RoomReservation.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        reservation.payment_status = True
        reservation.total_price = str(reservation.total_price)
        reservation.save()

        return Response({
            "room_reservation": RoomReservationSerializer(reservation, context=self.get_serializer_context()).data
        })


# View Set to update check in
class RoomCheckInViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RoomReservationSerializer

    def post(self, request, *args, **kwargs):
        if not is_staff(request.user, 2):
            raise serializers.ValidationError("Access Denied: You are not a receptionist")

        data = request.data
        reservation_id = data['reservation_id']

        try:
            reservation = RoomReservation.objects.get(id=reservation_id)
        except RoomReservation.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        reservation.checked_in = True
        reservation.total_price = float(str(reservation.total_price))
        reservation.save()

        return Response({
            "room_reservation": RoomReservationSerializer(reservation, context=self.get_serializer_context()).data
        })


# View Set to update check out
class RoomCheckOutViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RoomReservationSerializer

    def post(self, request, *args, **kwargs):
        if not is_staff(request.user, 2):
            raise serializers.ValidationError("Access Denied: You are not a receptionist")

        data = request.data
        reservation_id = data['reservation_id']

        try:
            reservation = RoomReservation.objects.get(id=reservation_id)
        except RoomReservation.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        reservation.checked_out = True
        reservation.total_price = float(str(reservation.total_price))
        reservation.save()

        return Response({
            "room_reservation": RoomReservationSerializer(reservation, context=self.get_serializer_context()).data
        })


# View Set to add a room review
class AddRoomReviewViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RoomReservationSerializer

    def post(self, request, *args, **kwargs):
        if not is_customer(request.user):
            raise serializers.ValidationError("Access Denied: You are not a customer")

        data = request.data
        reservation_id = data['reservation_id']
        try:
            reservation = RoomReservation.objects.get(id=reservation_id, customer=request.user.id)
        except RoomReservation.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        reservation.customer_review = data['customer_review']
        reservation.total_price = float(str(reservation.total_price))
        reservation.save()

        return Response({
            "room_reservation": RoomReservationSerializer(reservation, context=self.get_serializer_context()).data
        })


def get_total_price(data):
    room_type = Room.objects.filter(id=data['room'])[0].type_id
    room_price = RoomType.objects.filter(id=room_type)[0].price

    s_y, s_m, s_d = list(map(int, data['start_date'][:10].strip().split('-')))
    s_h, s_mi, s_s = list(map(int, data['start_date'][11:].strip().split(':')))
    e_y, e_m, e_d = list(map(int, data['end_date'][:10].strip().split('-')))
    e_h, e_mi, e_s = list(map(int, data['end_date'][11:].strip().split(':')))

    num_of_days = date(e_y, e_m, e_d) - date(s_y, s_m, s_d)

    return num_of_days.days * float(str(room_price)), datetime(s_y, s_m, s_d, s_h, s_mi, s_s), datetime(e_y, e_m, e_d,
                                                                                                        e_h, e_mi, e_s)


def are_dates_booked(start_date, end_date, room_id):
    prev_reservations_from_start = RoomReservation.objects.filter(room=room_id, start_date__lte=start_date,
                                                                  end_date__gt=start_date)
    if len(prev_reservations_from_start) == 0:
        prev_reservations_from_end = RoomReservation.objects.filter(room=room_id, start_date__lt=end_date,
                                                                    end_date__gte=end_date)
        if len(prev_reservations_from_end) == 0:
            return False
    return True
