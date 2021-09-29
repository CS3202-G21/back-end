from django.http import QueryDict
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import StaffSerializer, LoginSatffSerializer, RegisterStaffSerializer
from django.contrib.auth.models import Group


# Login API
class LoginStaffAPI(generics.GenericAPIView):
    serializer_class = LoginSatffSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff_member = serializer.validated_data
        group = staff_member.groups.all()

        return Response({
            "user": StaffSerializer(staff_member, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(staff_member)[1],
            "user_class": group[0].id
        })


# Get Staff User API
class StaffAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = StaffSerializer

    def get_object(self):
        return self.request.user


# Register API (for testing only)
class RegisterStaffAPI(generics.GenericAPIView):
    serializer_class = RegisterStaffSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        group_name = data.pop('group')

        group = Group.objects.create(name=group_name)

        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)


        serializer = self.get_serializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()

        group.user_set.add(staff)

        return Response({
            "user": StaffSerializer(staff, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(staff)[1],
            "user_class": staff.groups.all()[0].id
        })