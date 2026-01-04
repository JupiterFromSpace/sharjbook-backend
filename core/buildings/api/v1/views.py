from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

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

        except Exception as e :
            logger.exception("errrrrrrrrrrrrrrrroooooooooooooooooor")
            return ServerErrorResponse.send()

    
    
class ShowBuildingsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user

            manager_buildings = Building.objects.filter(manager=user)
            resident_buildings = Building.objects.filter(
                building_residents__resident=user,
                building_residents__is_approved=True
            )

            buildings = (manager_buildings | resident_buildings).distinct()
            serializer = BuildingListSerializer(buildings, many=True , context={"request":request})

            return SuccessResponse.send(
                message="لیست ساختمان‌ها با موفقیت دریافت شد",
                data=serializer.data
            )

        except Exception:
            return ServerErrorResponse.send()





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
