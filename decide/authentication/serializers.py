from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'is_superuser', 'is_staff')
        read_only_fields = ('is_active','is_superuser')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}
