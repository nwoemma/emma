# contact/serializers.py
from rest_framework import serializers

class BasicResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
