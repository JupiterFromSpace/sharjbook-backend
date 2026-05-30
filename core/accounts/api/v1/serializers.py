from rest_framework import serializers
from accounts.models import User, Profile



class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not value.startswith("+98"):
            raise serializers.ValidationError(
                "شماره موبایل باید با +98 شروع شود"
            )

        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate_phone(self, value):
        if not value.startswith("+98"):
            raise serializers.ValidationError(
                "شماره موبایل باید با +98 شروع شود"
            )

        return value


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Update profile fields partially (optional fields)."""

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
        read_only_fields = ["phone"]
