from rest_framework import serializers
from accounts.models import User, Profile



class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Update profile fields partially (optional fields)."""

    email = serializers.EmailField(source="user.email", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "image",
            "phone",
            "email",
            "discription",
        )
        read_only_fields = ["phone", "email"]
