from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from finance.models import Debt
from buildings.models import Building, BuildingResident
from core.utils.responses import (
    SuccessResponse,
    ErrorResponse,
    ServerErrorResponse
)
from .serializers import (
    CreateBuildingSerializer,
    BuildingListSerializer,
    AddResidentSerializer,
    ListResidentSerializer,
    ResidentTransferSerializer,
)

import logging
logger = logging.getLogger(__name__)



class CreateBuildingView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            serializer = CreateBuildingSerializer(
                data=request.data,
                context={"request": request}
        )


            if not serializer.is_valid():
                return ErrorResponse.send(
                    message="اطلاعات وارد شده نامعتبر است",
                    errors=serializer.errors
                )

            building = serializer.save()

            return SuccessResponse.send(
                message="ساختمان با موفقیت ایجاد شد",
                data={
                    "building_id": building.id,
                    "name": building.name
                },
                status_code=201
            )

        except Exception :
            return ServerErrorResponse.send()

    
    
class ShowBuildingsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        buildings = (
            Building.objects
            .filter(
                Q(manager=user) |
                Q(
                    building_residents__resident=user,
                    building_residents__is_approved=True
                )
            )
            .select_related("manager")
            .prefetch_related("building_residents")
            .distinct()
        )

        serializer = BuildingListSerializer(
            buildings,
            many=True,
            context={"request": request}
        )

        return SuccessResponse.send(
            message="لیست ساختمان‌ها با موفقیت دریافت شد",
            data=serializer.data
        )





class AddResidentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, building_id):
        try:
            try:
                building = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                return ErrorResponse.send(
                    message="ساختمان یافت نشد",
                    status_code=404
                )

            if building.manager_id != request.user.id:
                return ErrorResponse.send(
                    message="شما مدیر این ساختمان نیستید",
                    status_code=403
                )

            serializer = AddResidentSerializer(
                data=request.data,
                context={"building": building, "request": request}
            )

            if not serializer.is_valid():
                return ErrorResponse.send(
                    message="اطلاعات وارد شده نامعتبر است",
                    errors=serializer.errors
                )

            resident = serializer.save()

            return SuccessResponse.send(
                message="ساکن با موفقیت اضافه شد",
                data={
                    "resident_id": resident.id,
                    "full_name": resident.resident.full_name,
                    "phone": resident.resident.phone,
                    "unit": resident.unit,
                    "monthly_charge_amount": str(resident.monthly_charge_amount),
                },
                status_code=201
            )

        except Exception:
            return ServerErrorResponse.send()





class ListResidentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListResidentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, building_id):
        try:
            try:
                building = Building.objects.get(id=building_id)
            except Building.DoesNotExist:
                return ErrorResponse.send(
                    message="ساختمان یافت نشد",
                    status_code=404
                )

            if building.manager_id != request.user.id:
                return ErrorResponse.send(
                    message="شما مدیر این ساختمان نیستید",
                    status_code=403
                )

            queryset = BuildingResident.objects.filter(
                building=building
            ).select_related("resident")

            paginator = ListResidentPagination()
            page = paginator.paginate_queryset(queryset, request)

            serializer = ListResidentSerializer(page, many=True)

            return SuccessResponse.send(
                message="لیست ساکنین با موفقیت دریافت شد",
                data=serializer.data
            )

        except Exception:
            return ServerErrorResponse.send()



class TransferDebtsView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, resident_id):
        """انتقال بدهی‌ها به مالک و بروزرسانی اطلاعات ساکن"""
        resident_relation = get_object_or_404(BuildingResident, pk=resident_id)
        resident = resident_relation.resident
        owner = resident_relation.building.manager

        serializer = ResidentTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # حداقل یکی از فیلدها باید تغییر کند
        if not any(field in data for field in ['first_name', 'last_name', 'phone']):
            return ErrorResponse.send(message="حداقل یکی از فیلدها باید تغییر کند")

        try:
            with transaction.atomic():
                # انتقال بدهی‌ها به مالک
                Debt.objects.filter(
                    building=resident_relation.building,
                    unit_number=resident_relation.unit,
                    responsible=resident
                ).update(responsible=owner)

                # بروزرسانی اطلاعات ساکن
                for field in ['first_name', 'last_name', 'phone']:
                    if field in data:
                        setattr(resident, field, data[field])
                resident.save()

            return SuccessResponse.send(
                message="اطلاعات ساکن بروزرسانی شد و بدهی‌ها به مالک منتقل شد."
            )

        except Exception as e:
            return ServerErrorResponse.send(message=str(e))