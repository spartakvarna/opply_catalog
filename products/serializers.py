from rest_framework import serializers


class CustomerAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
