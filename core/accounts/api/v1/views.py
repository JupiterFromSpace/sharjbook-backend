from .serializers import LoginSerializer
from rest_framework import generics


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
