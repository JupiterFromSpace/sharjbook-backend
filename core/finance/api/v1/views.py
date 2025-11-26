from rest_framework import generics
from .serializers import ListBuildingFundSerializer , ShowDemandFromResidentsSerializer,ShowDebtorsListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db import models
from finance.models import BuildingFund, Debt

class ListBuildingFundView(generics.ListAPIView):
    serializer_class = ListBuildingFundSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        
        if user.is_manager:
            # فقط صندوق ساختمان‌های خودش
            return BuildingFund.objects.filter(building__manager=user)

        if user.is_resident:
            # اگر بخوای ساکن فقط صندوق ساختمان خودش رو ببینه
            return BuildingFund.objects.filter(building__residents=user).distinct()

        return BuildingFund.objects.none()

    
    
    
    
class ShowDemandFromResidentsView(generics.ListAPIView):
    serializer_class = ShowDemandFromResidentsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        
        if user.is_manager:
            return Debt.objects.filter(building__manager=user)

        if user.is_resident:
            return Debt.objects.filter(resident=user)

        return Debt.objects.none()

    
    
    
    
class ShowDebtorsListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
       
class ShowDebtorsListView(generics.ListAPIView):
    serializer_class = ShowDebtorsListSerializer
    pagination_class = ShowDebtorsListPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        
        if user.is_manager:
            return Debt.objects.filter(
                is_paid=False
            ).filter(
                models.Q(building__manager=user) | models.Q(resident=user)
            )

        if user.is_resident:
            return Debt.objects.filter(
                is_paid=False,
                resident=user
            )

        return Debt.objects.none()
