from rest_framework import serializers

from django.contrib.auth.models import User
from census.models import Census

class CensusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Census
        fields = ('id', 'voting_id', 'voter_id')

class UserAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

