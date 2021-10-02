from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth.models import User
from .serializers import CustomerSerializer, RegisterCustomerSerializer, LoginCustomerSerializer


# Register API
class RegisterCustomerAPI(generics.GenericAPIView):
    serializer_class = RegisterCustomerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response({
            "user": CustomerSerializer(customer, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(customer)[1],
            "user_class": 0
        })


# Login API
class LoginCustomerAPI(generics.GenericAPIView):
    serializer_class = LoginCustomerSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.validated_data
        return Response({
            "user": CustomerSerializer(customer, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(customer)[1],
            "user_class": 0
        })


# Get Customer User API
class CustomerAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = CustomerSerializer

    def get_object(self):
        return self.request.user


# Get Customer User from ID
class GetUserFromIDAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = CustomerSerializer

    def get(self, request, user_id):
        user_info = User.objects.get(id=user_id)
        user_dict = user_info.__dict__

        user = {'id': user_dict['id'], 'username': user_dict['username'], 'first_name': user_dict['first_name'], 'last_name': user_dict['last_name'], 'email': user_dict['email']}

        return Response({
            "user": user,
            "user_class": 0
        })
