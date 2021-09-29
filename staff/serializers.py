from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# Login Staff Serializer
class LoginSatffSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            group = user.groups.all()
            if group:
                return user
        raise serializers.ValidationError("Incorrect Credentials")


# Register Staff Serializer (for testing only)
class RegisterStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        staff = User.objects.create_user(validated_data['username'], validated_data['email'],
                                         validated_data['password'])
        staff.first_name = validated_data['first_name']
        staff.last_name = validated_data['last_name']
        staff.is_staff = True
        staff.save()

        return staff
