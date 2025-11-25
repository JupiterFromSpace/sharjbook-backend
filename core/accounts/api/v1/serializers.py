from rest_framework import serializers
from accounts.models import User

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        User.phone_validator(value)
        return value

    def create(self, validated_data):
        phone = validated_data['phone']
        user, created = User.objects.get_or_create(phone=phone)
        return user
