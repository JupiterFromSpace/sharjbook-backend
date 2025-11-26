from django.urls import path
from .views import ListBuildingFundView , ShowDemandFromResidentsView , ShowDebtorsListView

app_name = 'finance'

urlpatterns = [
    path('show-fund/', ListBuildingFundView.as_view(), name='list-building-fund'),
    path('demand-from-residents/', ShowDemandFromResidentsView.as_view(), name='demand-from-residents'),
    path('debtors-list/', ShowDebtorsListView.as_view(), name='debtors-list'),
]
