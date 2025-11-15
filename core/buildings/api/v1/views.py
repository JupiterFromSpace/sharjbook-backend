from rest_framework import generics
from django.contrib.auth import get_user_model
from buildings.models import Building
from .serializers import CreateBuildingSerializer, BuildingListSerializer


class CreateBuildingView(generics.CreateAPIView):
    queryset = Building.objects.all()
    serializer_class = CreateBuildingSerializer
    
    
User = get_user_model()
    
class ShowBuildingsView(generics.ListAPIView):
    serializer_class = BuildingListSerializer
    
    def get_queryset(self):
        # فعلاً چون لاگین نداری:
        user = User.objects.get(username="user1") 
        # بعداً میشه: user = self.request.user

        if user.role == "MANAGER":
            # ساختمان‌هایی که این فرد مدیرشون هست
            return Building.objects.filter(manager=user)

        if user.role == "RESIDENT":
            # ساختمان‌هایی که این فرد ساکن آن‌هاست
            return Building.objects.filter(residents=user)

        return Building.objects.none()