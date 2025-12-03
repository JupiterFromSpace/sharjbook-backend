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

        # اگر مدیر یا ساکن هنوز ساختمان فعال انتخاب نکرده
        if not hasattr(user, "active_building") or user.active_building is None:
            return BuildingFund.objects.none()

        # فقط صندوق ساختمان انتخاب‌شده را برگردان
        return BuildingFund.objects.filter(building=user.active_building)


    
    
    
    
class ShowDemandFromResidentsView(generics.ListAPIView):
    serializer_class = ShowDemandFromResidentsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        if not user.active_building:
            return Debt.objects.none()

        # اگر مدیر است → بدهی همهٔ ساکنین همان ساختمان فعال
        if user.is_manager:
            return Debt.objects.filter(
                building=user.active_building
            )

        # اگر ساکن است → فقط بدهی خودش در ساختمان فعال
        return Debt.objects.filter(
            building=user.active_building,
            resident=user
        )

    
    
    
    
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

        if not user.active_building:
            return Debt.objects.none()

        # مدیر → تمام بدهکاران ساختمان فعال
        if user.is_manager:
            return Debt.objects.filter(
                building=user.active_building,
                is_paid=False
            )

        # ساکن → فقط بدهی خودش در ساختمان فعال
        return Debt.objects.filter(
            building=user.active_building,
            resident=user,
            is_paid=False
        )
