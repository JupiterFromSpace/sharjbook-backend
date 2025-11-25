from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User


class LoginView(APIView):

    def post (self,request):
        phone = request.data.get('phone')
        
        if not phone:
            return Response({'error': 'شماره تلفن الزامی است'}, status=400)
        
        user, created = User.objects.get_or_create(phone=phone)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user_id": user.id,
            "phone": user.phone,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })