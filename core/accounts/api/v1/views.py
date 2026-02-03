from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer, UpdateProfileSerializer
from core.utils.responses import SuccessResponse, ErrorResponse, ServerErrorResponse
from ...models.profiles import Profile

class LoginView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'login'
    
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
                "phone": user.phone,
                "access": str(refresh.access_token),
                "refresh":str(refresh)
            }
        )
        
        return response



class RefreshTokenView(APIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'refresh'
    
    def post(self, request):
        refresh_token = request.get("refresh")

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


# repair this endpoint !
class LogoutView(APIView):
    throttle_scope = 'logout'
    
    def post(self, request):
        response = SuccessResponse.send(
            message="خروج با موفقیت انجام شد"
        )
        response.delete_cookie("refresh")
        return response
    
    


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    """Update user profile with optional fields."""
    
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer

    
    def get_object(self):
        return self.request.user.profile
    
    def patch(self,request,*args,**kwargs):
        try:
            profile = self.get_object()
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return SuccessResponse.send(
                data = serializer.data,
                message= "پروفایل با موفقیت تغییر یافت"
            )
        except Profile.DoesNotExist:
            return ErrorResponse.send(
                status_code= 400,
                message="پروفایل پیدا نشد"
            )
        except Exception:
            return ServerErrorResponse()