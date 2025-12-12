from rest_framework import generics, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from buildings.models import Building
from .serializers import (CreateBuildingSerializer, BuildingListSerializer, SelectActiveBuildingSerializer,
    AddResidentSerializer,    
    )


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



class SelectActiveBuildingView(generics.GenericAPIView):
    serializer_class = SelectActiveBuildingSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        building = serializer.validated_data["building"]

        request.user.active_building = building
        request.user.save()

        return Response({"message": "ساختمان فعال تنظیم شد."})




class AddResidentView(generics.GenericAPIView):
    serializer_class = AddResidentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, building_id):
        manager = request.user

        try:
            building = Building.objects.get(id=building_id)
        except Building.DoesNotExist:
            return Response({"error": "ساختمان یافت نشد."}, status=404)

        if building.manager_id != manager.id:
            return Response({"error": "شما مدیر این ساختمان نیستید."}, status=403)

        serializer = self.get_serializer(
            data=request.data,
            context={"building": building, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        resident = serializer.save()

        return Response({
            "message": "ساکن با موفقیت اضافه شد.",
            "resident_id": resident.id,
            "full_name": resident.resident.full_name,
            "phone": resident.resident.phone,
            "unit": resident.unit,
            "monthly_charge_amount": str(resident.monthly_charge_amount),
        }, status=201)
