from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

from .serializers import RequestOTPSerializer, VerifyOTPSerializer, UpdateProfileSerializer, EmailPasswordLoginSerializer
from core.utils.responses import SuccessResponse, ErrorResponse, ServerErrorResponse
from ...models.profiles import Profile
from accounts.models import User, OTP


class EmailPasswordLoginView(APIView):
    """
    ورود با ایمیل و رمز عبور - برای تست Swagger
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = EmailPasswordLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse.send(
                message="اطلاعات وارد شده نامعتبر است",
                errors=serializer.errors,
                status_code=400,
            )

        email    = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user     = authenticate(request, username=email, password=password)

        if user is None:
            return ErrorResponse.send(message="ایمیل یا رمز عبور اشتباه است", status_code=401)

        refresh = RefreshToken.for_user(user)

        return SuccessResponse.send(
            message="ورود با موفقیت انجام شد",
            data={
                "email": user.email,
                "role": user.role,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        )


class RequestOTPView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = "login"

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse.send(
                message="اطلاعات وارد شده نامعتبر است",
                errors=serializer.errors,
            )

        phone = serializer.validated_data["phone"]

        try:
            user, _ = User.objects.get_or_create(phone=phone)
            code = OTP.generate_code()
            OTP.objects.create(user=user, code=code)

            return SuccessResponse.send(message="کد تایید به شماره موبایل شما ارسال شد")

        except Exception as e:
            return ServerErrorResponse()


class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = "login"

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse.send(
                message="اطلاعات وارد شده نامعتبر است",
                errors=serializer.errors,
            )

        phone = serializer.validated_data["phone"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return ErrorResponse.send(message="کاربر یافت نشد", status_code=404)

        otp = (
            OTP.objects.filter(user=user, code=code, is_used=False)
            .order_by("-created_at")
            .first()
        )

        if not otp:
            return ErrorResponse.send(message="کد تایید نامعتبر است", status_code=400)

        if otp.is_expired():
            return ErrorResponse.send(message="کد تایید منقضی شده است", status_code=400)

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        refresh = RefreshToken.for_user(user)

        return SuccessResponse.send(
            message="ورود با موفقیت انجام شد",
            data={
                "phone": user.phone,
                "role": user.role,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        )


class RefreshTokenView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = "refresh"

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return ErrorResponse.send(message="توکن رفرش یافت نشد", status_code=401)

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            return SuccessResponse.send(
                data={"access": str(access)}, message="توکن جدید صادر شد"
            )
        except Exception:
            return ErrorResponse.send(message="توکن نامعتبر است", status_code=401)


class LogoutView(APIView):
    throttle_scope = "logout"

    def post(self, request):
        response = SuccessResponse.send(message="خروج با موفقیت انجام شد")
        response.delete_cookie("refresh")
        return response


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, *args, **kwargs):
        try:
            profile = self.get_object()
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return SuccessResponse.send(
                data=serializer.data, message="پروفایل با موفقیت تغییر یافت"
            )
        except Profile.DoesNotExist:
            return ErrorResponse.send(status_code=400, message="پروفایل پیدا نشد")
        except Exception:
            return ServerErrorResponse()
