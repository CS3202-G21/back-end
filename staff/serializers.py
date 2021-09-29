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
