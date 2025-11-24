from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from buildings.models import Building
from .serializers import CreateBuildingSerializer, BuildingListSerializer


class CreateBuildingView(generics.CreateAPIView):
    serializer_class = CreateBuildingSerializer
    
    
User = get_user_model()
    
class ShowBuildingsView(generics.ListAPIView):
    serializer_class = BuildingListSerializer

    def get_queryset(self):
        return Building.objects.all()

    def list(self, request, *args, **kwargs):
        phone = request.query_params.get("phone")
        if not phone:
            raise ValidationError({"phone": "شماره تلفن الزامی است."})

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise ValidationError({"phone": "کاربری با این شماره تلفن یافت نشد."})

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={"user": user})
        return Response(serializer.data)