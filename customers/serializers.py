from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# Register Customer Serializer
class RegisterCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        customer.first_name = validated_data['first_name']
        customer.last_name = validated_data['last_name']
        customer.save()

        return customer


# Login Customer Serializer
class LoginCustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            group = user.groups.all()
            if not group:
                return user
        raise serializers.ValidationError("Incorrect Credentials")

