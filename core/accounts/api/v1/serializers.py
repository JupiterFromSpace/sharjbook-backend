from rest_framework import serializers
from accounts.models import User,Profile

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone",)
        extra_kwargs = {
            "phone": {
                "validators":[]
            }
        }

    def create(self, validated_data):
        phone = validated_data["phone"]

        user, created = User.objects.get_or_create(phone=phone)

        self.context["created"] = created

        return user







class UpdateProfileSerializer(serializers.ModelSerializer):
    """Update profile fields partially (optional fields)."""
    
    phone = serializers.CharField(source="user.phone", read_only=True)
    
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'image',
            'phone',
            'email',
            'discription',
        )
        read_only_fields = ['phone']