from .models import RoomReservation
from rooms.models import Room
from django.contrib.auth.models import User
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
        room_reservations = get_reservation_list(room_reservations_objs)

        return Response({"room_reservations": room_reservations})

    def post(self, request, *args, **kwargs):
        data = request.data

        if is_customer(request.user):
            data['customer'] = request.user.id
        elif is_staff(request.user, "Receptionist"):
            data['customer'] = User.objects.get(username=data['customer']).id
        else:
            raise serializers.ValidationError("Access Denied: You are not a customer or a receptionist.")

        data['total_price'], start_date, end_date = get_total_price(data)

        if are_dates_booked(start_date, end_date, data['room']):
            raise serializers.ValidationError("Given Dates are Booked")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        room_reservation = serializer.save()

        return Response({
            "room_reservation": RoomReservationSerializer(room_reservation, context=self.get_serializer_context()).data
        })


# View Set to get the available reservations (check-in and check-out) for today
class GetTodayRoomReservationsViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RoomReservationSerializer

    def get(self, request):
        if not is_staff(request.user, "Receptionist"):
            raise serializers.ValidationError("Access Denied: You are not a receptionist")

        today = datetime.now().date()

        check_in_reservation_objs = RoomReservation.objects.filter(start_date=today)
        check_out_reservation_objs = RoomReservation.objects.filter(end_date=today)

        check_in_reservations = get_reservation_list(check_in_reservation_objs)
        check_out_reservations = get_reservation_list(check_out_reservation_objs)

        return Response({"check_in_reservations": check_in_reservations, "check_out_reservations": check_out_reservations})


# View Set to get the reviews
class GetRoomReviewsViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RoomReservationSerializer

    def get(self, request):
        reviews = RoomReservation.objects.exclude(customer_review="").values('customer', 'room_id', 'customer_review')

        return Response({"reviews": reviews})


# View Set to update payment success
class RoomReservationSuccessViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = RoomReservationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        if is_customer(request.user):
            data['customer'] = request.user.id
        elif is_staff(request.user, "Receptionist"):
            data['customer'] = User.objects.get(username=data['customer']).id
        else:
            raise serializers.ValidationError("Access Denied: You are not a customer or a receptionist.")

        reservation_id = data['reservation_id']

        try:
            reservation = RoomReservation.objects.get(id=reservation_id, customer=data['customer'])
        except RoomReservation.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        reservation.payment_status = True
        reservation.total_price = float(str(reservation.total_price))
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
        if not is_staff(request.user, "Receptionist"):
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
        if not is_staff(request.user, "Receptionist"):
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
    e_y, e_m, e_d = list(map(int, data['end_date'][:10].strip().split('-')))

    num_of_days = date(e_y, e_m, e_d) - date(s_y, s_m, s_d)

    return num_of_days.days * float(str(room_price)), date(s_y, s_m, s_d), date(e_y, e_m, e_d)


def are_dates_booked(start_date, end_date, room_id):
    prev_reservations_from_start = RoomReservation.objects.filter(room=room_id, start_date__lte=start_date,
                                                                  end_date__gt=start_date)
    if len(prev_reservations_from_start) == 0:
        prev_reservations_from_end = RoomReservation.objects.filter(room=room_id, start_date__lt=end_date,
                                                                    end_date__gte=end_date)
        if len(prev_reservations_from_end) == 0:
            return False
    return True


def get_reservation_list(reservation_objs):
    room_reservations = []

    for obj in reservation_objs:
        reservation = obj.__dict__
        reservation.pop('_state')
        reservation['total_price'] = float(str(reservation['total_price']))
        room_reservations.append(reservation)

    return room_reservations
