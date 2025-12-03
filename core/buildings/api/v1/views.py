from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from buildings.models import Building
from .serializers import CreateBuildingSerializer, BuildingListSerializer, SelectActiveBuildingSerializer


class CreateBuildingView(generics.CreateAPIView):
    serializer_class = CreateBuildingSerializer
    permission_classes = (IsAuthenticated,)
    
User = get_user_model()
    
class ShowBuildingsView(generics.ListAPIView):
    serializer_class = BuildingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        manager_buildings = Building.objects.filter(manager=user)

        resident_buildings = Building.objects.filter(
            building_residents__resident=user,
            building_residents__is_approved=True
        )

        return (manager_buildings | resident_buildings).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)


class SelectActiveBuildingView(generics.GenericAPIView):
    serializer_class = SelectActiveBuildingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        building = serializer.validated_data["building"]

        request.user.active_building = building
        request.user.save()

        return Response({"message": "ساختمان فعال تنظیم شد."})
