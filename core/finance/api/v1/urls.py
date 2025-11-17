from django.urls import path
from .views import ListBuildingFundView , showDemandFromResidentsView

app_name = 'finance'

urlpatterns = [
    path('show-fund/', ListBuildingFundView.as_view(), name='list-building-fund'),
    path('demand-from-residents/', showDemandFromResidentsView.as_view(), name='demand-from-residents'),
]
