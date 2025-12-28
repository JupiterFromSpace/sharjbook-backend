from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import (ListBuildingFundSerializer , ShowDemandFromResidentsSerializer, ShowDebtorsListSerializer 
 , TransactionListSerializer)
from rest_framework.exceptions import NotFound
from finance.models import BuildingFund, Debt, Transaction
from buildings. models import Building

##______________________

from rest_framework.exceptions import NotFound, PermissionDenied
from buildings.models import Building

def get_building_for_user(user, building_id):
    try:
        building = Building.objects.get(id=building_id)
    except Building.DoesNotExist:
        raise NotFound("ساختمان یافت نشد")

    # مدیر
    if building.manager == user:
        return building

    # ساکن تأیید شده
    if building.building_residents.filter(
        resident=user,
        is_approved=True
    ).exists():
        return building

    raise PermissionDenied("شما به این ساختمان دسترسی ندارید")
##_____________________________________________________



class ListBuildingFundView(generics.ListAPIView):
    serializer_class = ListBuildingFundSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        building_id = self.kwargs.get("building_id")

        building = get_building_for_user(user, building_id)

        return BuildingFund.objects.filter(building=building)




    
    
    
    
class ShowDemandFromResidentsView(generics.ListAPIView):
    serializer_class = ShowDemandFromResidentsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        building_id = self.kwargs.get("building_id")

        building = get_building_for_user(user, building_id)

        return Debt.objects.filter(building=building)


    
    
    
    
class ListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
       
class ShowDebtorsListView(generics.ListAPIView):
    serializer_class = ShowDebtorsListSerializer
    pagination_class = ListPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        building_id = self.kwargs.get("building_id")

        building = get_building_for_user(user, building_id)

        return Debt.objects.filter(
            building=building,
            is_paid=False
        )




class ListIncomeTransactionsView(generics.ListAPIView):
    '''Endpoint List of income'''
    serializer_class = TransactionListSerializer
    pagination_class = ListPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        building_id = self.kwargs.get("building_id")

        building = get_building_for_user(user, building_id)

        return Transaction.objects.filter(
            building=building,
            transaction_type=Transaction.TransactionTypes.INCOME
        )

        
        

class ListExpenseTransactionsView(generics.ListAPIView):
    '''Endpoint expense List'''
    serializer_class = TransactionListSerializer
    pagination_class = ListPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        building_id = self.kwargs.get("building_id")

        building = get_building_for_user(user, building_id)

        return Transaction.objects.filter(
            building=building,
            transaction_type=Transaction.TransactionTypes.EXPENSE
        )
