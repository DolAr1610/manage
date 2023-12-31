from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CustomUserCreateSerializer(UserCreateSerializer):
    """Registration user"""
    re_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "re_password")
        extra_kwargs = {"password": {"write_only": True, "required": True, "validators": [validate_password]}, }

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError({"re_password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user
