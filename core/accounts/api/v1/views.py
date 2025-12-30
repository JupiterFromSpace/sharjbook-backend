from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer
from core.utils.responses import SuccessResponse, ErrorResponse


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse.send(
                message="اطلاعات وارد شده نامعتبر است",
                errors=serializer.errors
            )

        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        response = SuccessResponse.send(
            message="ورود با موفقیت انجام شد",
            data={
                "user_id": str(user.id),
                "phone": user.phone,
                "access": str(refresh.access_token),
            }
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=True,          
            samesite="Lax",    
            max_age=60 * 60 * 24 * 7 
        )

        return response



class RefreshTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return ErrorResponse.send(
                message="توکن رفرش یافت نشد",
                status_code=401
            )

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

            return SuccessResponse.send(
                data={"access": str(access)},
                message="توکن جدید صادر شد"
            )

        except Exception:
            return ErrorResponse.send(
                message="توکن نامعتبر است",
                status_code=401
            )



class LogoutView(APIView):
    def post(self, request):
        response = SuccessResponse.send(
            message="خروج با موفقیت انجام شد"
        )
        response.delete_cookie("refresh")
        return response
