from rest_framework import serializers


class BackupSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=200)

