from rest_framework import serializers
from accounts.models import User

class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['phone']

    def create(self, validated_data):
        phone = validated_data['phone']
        user, created = User.objects.get_or_create(phone=phone)
        return user