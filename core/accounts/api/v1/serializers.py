from rest_framework import serializers
from accounts.models import User, Profile


class RequestOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not value.startswith("+98") or len(value) != 13:
            raise serializers.ValidationError(
                "شماره موبایل باید با +98 شروع شود. مثال: +989123456789"
            )
        return value


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate_phone(self, value):
        if not value.startswith("+98") or len(value) != 13:
            raise serializers.ValidationError(
                "شماره موبایل باید با +98 شروع شود. مثال: +989123456789"
            )
        return value


class EmailPasswordLoginSerializer(serializers.Serializer):
    email    = serializers.EmailField(help_text="ایمیل کاربر")
    password = serializers.CharField(write_only=True, help_text="رمز عبور")


class UpdateProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.EmailField(source="user.email", required=False)

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
