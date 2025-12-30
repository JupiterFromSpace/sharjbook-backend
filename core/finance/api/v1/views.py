from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from finance.models import BuildingFund, Debt, Transaction
from buildings.models import Building

from core.utils.responses import (
    SuccessResponse,
    ErrorResponse,
    ServerErrorResponse
)

from .serializers import (
    ListBuildingFundSerializer,
    ShowDemandFromResidentsSerializer,
    ShowDebtorsListSerializer,
    TransactionListSerializer
)

#______________________


def get_building_for_user(user, building_id):
    try:
        building = Building.objects.get(id=building_id)
    except Building.DoesNotExist:
        return None, ErrorResponse.send(
            message="ساختمان یافت نشد",
            status_code=404
        )

    if building.manager == user:
        return building, None

    if building.building_residents.filter(
        resident=user,
        is_approved=True
    ).exists():
        return building, None

    return None, ErrorResponse.send(
        message="شما به این ساختمان دسترسی ندارید",
        status_code=403
    )

#_____________________________________________________



class ListBuildingFundView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, building_id):
        try:
            building, error = get_building_for_user(request.user, building_id)
            if error:
                return error

            funds = BuildingFund.objects.filter(building=building)
            serializer = ListBuildingFundSerializer(funds, many=True)

            return SuccessResponse.send(
                message="اطلاعات صندوق ساختمان با موفقیت دریافت شد",
                data=serializer.data
            )

        except Exception:
            return ServerErrorResponse.send()



    
    
    
    
class ShowDemandFromResidentsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, building_id):
        try:
            building, error = get_building_for_user(request.user, building_id)
            if error:
                return error

            debts = Debt.objects.filter(building=building)
            serializer = ShowDemandFromResidentsSerializer(debts, many=True)

            return SuccessResponse.send(
                message="لیست بدهی‌ها با موفقیت دریافت شد",
                data=serializer.data
            )

        except Exception:
            return ServerErrorResponse.send()



    
    
    
    
class ListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
       
class ShowDebtorsListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, building_id):
        try:
            building, error = get_building_for_user(request.user, building_id)
            if error:
                return error

            queryset = Debt.objects.filter(
                building=building,
                is_paid=False
            )

            paginator = ListPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = ShowDebtorsListSerializer(page, many=True)

            return SuccessResponse.send(
                message="لیست بدهکاران با موفقیت دریافت شد",
                data=serializer.data
            )

        except Exception:
            return ServerErrorResponse.send()





class ListIncomeTransactionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, building_id):
        try:
            building, error = get_building_for_user(request.user, building_id)
            if error:
                return error

            queryset = Transaction.objects.filter(
                building=building,
                transaction_type=Transaction.TransactionTypes.INCOME
            )

            paginator = ListPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = TransactionListSerializer(page, many=True)

            return SuccessResponse.send(
                message="لیست درآمدها با موفقیت دریافت شد",
                data=serializer.data
            )

        except Exception:
            return ServerErrorResponse.send()


        
        

class ListExpenseTransactionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, building_id):
        try:
            building, error = get_building_for_user(request.user, building_id)
            if error:
                return error

            queryset = Transaction.objects.filter(
                building=building,
                transaction_type=Transaction.TransactionTypes.EXPENSE
            )

            paginator = ListPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = TransactionListSerializer(page, many=True)

            return SuccessResponse.send(
                message="لیست هزینه‌ها با موفقیت دریافت شد",
                data=serializer.data
            )

        except Exception:
            return ServerErrorResponse.send()

