from .models import CustomerOrder
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CustomerOrderSerializer
from rest_framework import serializers
from middleware.user_group_validation import is_customer, is_staff
from middleware.enums.order_status_enum import order_statuses
from middleware.current_meal_times import current_times
import json


# Customer Order ViewSet
class CustomerOrderViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CustomerOrderSerializer

    def get(self, request):
        if not is_customer(request.user):
            raise serializers.ValidationError("Access Denied: You are not a customer")

        orders_objs = CustomerOrder.objects.filter(customer=request.user.id)
        orders = get_order_list(orders_objs)

        return Response({"orders": orders})

    def post(self, request, *args, **kwargs):
        if not is_staff(request.user, "Virtual Waiter"):
            raise serializers.ValidationError("Access Denied: You are not a virtual waiter")

        data = request.data
        data['customer'] = User.objects.filter(username=data['customer'])[0].id

        try:
            data['id'] = CustomerOrder.objects.order_by('-id')[0].id + 1
        except IndexError:
            data['id'] = 1

        data['menu_items'] = json.dumps(data['menu_items'])
        data['special_offers'] = json.dumps(data['special_offers'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response({
            "order": CustomerOrderSerializer(order, context=self.get_serializer_context()).data
        })


# View Set to get the available orders for today
class GetCustomerOrdersViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CustomerOrderSerializer

    def get(self, request):
        if not (is_staff(request.user, "Waiter") or is_staff(request.user, "Chef")):
            raise serializers.ValidationError("Access Denied: You are not a waiter or a chef")

        # restaurant = request.data['restaurant']

        today = datetime.now()
        time_now = today.time()
        breakfast_begin, breakfast_end, lunch_begin, lunch_end, dinner_begin, dinner_end = current_times

        if breakfast_begin <= time_now <= breakfast_end:
            order_objs = CustomerOrder.objects.filter(date_created__gt=today.replace(hour=0, minute=1, second=0),
                                                      date_created__lt=today.replace(hour=13, minute=0, second=0))
        elif lunch_begin <= time_now <= lunch_end:
            order_objs = CustomerOrder.objects.filter(date_created__gt=today.replace(hour=13, minute=0, second=0),
                                                      date_created__lt=today.replace(hour=17, minute=30, second=0))
        elif dinner_begin <= time_now <= dinner_end:
            order_objs = CustomerOrder.objects.filter(date_created__gt=today.replace(hour=17, minute=30, second=0),
                                                      date_created__lt=today.replace(hour=23, minute=59, second=0))
        else:
            raise serializers.ValidationError("No Meal Provided at this Time.")

        orders = get_order_list(order_objs)

        return Response({"orders": orders})


# View Set to get update customer order status
class CustomerOrderUpdateViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CustomerOrderSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        order_id = data['order_id']
        try:
            order = CustomerOrder.objects.get(id=order_id)
            order_status = order.status
        except CustomerOrder.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        if is_staff(request.user, "Waiter"):
            if order_status == order_statuses[3][0]:
                order.status = order_statuses[4][0]
            elif order_status == order_statuses[4][0]:
                order.status = order_statuses[5][0]
            else:
                raise serializers.ValidationError("Waiters cannot update order status at " + order_status + " state.")
        elif is_staff(request.user, "Chef"):
            if order_status == order_statuses[0][0]:
                order.status = order_statuses[1][0]
            elif order_status == order_statuses[1][0]:
                order.status = order_statuses[2][0]
            elif order_status == order_statuses[2][0]:
                order.status = order_statuses[3][0]
            else:
                raise serializers.ValidationError("Chefs cannot update order status at " + order_status + " state.")
        else:
            raise serializers.ValidationError("Access Denied: You are not a waiter or a chef")

        order.total_price = float(str(order.total_price))
        order.save()

        return Response({
            "order": CustomerOrderSerializer(order, context=self.get_serializer_context()).data
        })


# View Set to update payment success
class CustomerOrderPaymentSuccessViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CustomerOrderSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        order_id = data['order_id']

        try:
            order = CustomerOrder.objects.get(id=order_id)
            order_status = order.status
        except CustomerOrder.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        if is_staff(request.user, "Virtual Waiter"):
            if order_status == order_statuses[5][0]:
                order.status = order_statuses[6][0]
            else:
                raise serializers.ValidationError(
                    "Virtual Waiters cannot update order status at " + order_status + " state.")
        else:
            raise serializers.ValidationError("Access Denied: You are not a virtual waiter.")

        order.total_price = float(str(order.total_price))
        order.save()

        return Response({
            "order": CustomerOrderSerializer(order, context=self.get_serializer_context()).data
        })


# View Set to add a review
class AddOrderReviewViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CustomerOrderSerializer

    def post(self, request, *args, **kwargs):
        if not is_staff(request.user, "Virtual Waiter"):
            raise serializers.ValidationError("Access Denied: You are not a virtual waiter")

        data = request.data
        data['customer'] = User.objects.filter(username=data['customer'])[0].id

        order_id = data['order_id']

        # print(data['customer'])

        try:
            order = CustomerOrder.objects.get(id=order_id, customer=data['customer'])
        except CustomerOrder.DoesNotExist:
            raise serializers.ValidationError("Invalid Access")

        order.customer_review = data['customer_review']
        order.total_price = float(str(order.total_price))
        order.save()

        return Response({
            "order": CustomerOrderSerializer(order, context=self.get_serializer_context()).data
        })


# View Set to get the reviews
class GetOrderReviewsViewSet(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CustomerOrderSerializer

    def get(self, request):
        reviews = CustomerOrder.objects.exclude(customer_review="").values('customer', 'restaurant', 'customer_review')

        return Response({"reviews": reviews})


def get_order_list(obj_list):
    orders = []

    for obj in obj_list:
        order = obj.__dict__
        order.pop('_state')
        order['total_price'] = float(str(order['total_price']))
        order['menu_items'] = json.loads(order['menu_items'])
        order['special_offers'] = json.loads(order['special_offers'])
        orders.append(order)

    return orders
