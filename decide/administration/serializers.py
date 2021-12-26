from rest_framework import serializers

from django.contrib.auth.models import User


class UserAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=1)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(allow_blank=True)
    email = serializers.EmailField()
