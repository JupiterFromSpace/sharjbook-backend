from rest_framework import generics
from .serializers import ListBuildingFundSerializer , ShowDemandFromResidents
from finance.models import BuildingFund, Debt

class ListBuildingFundView(generics.ListAPIView):
    
    serializer_class = ListBuildingFundSerializer
    queryset = BuildingFund.objects.all()
    
class showDemandFromResidentsView(generics.ListAPIView):
    
    serializer_class = ShowDemandFromResidents
    queryset = Debt.objects.all()