from rest_framework import serializers
from finance.models import BuildingFund , Debt


class ListBuildingFundSerializer(serializers.ModelSerializer):
    '''Serializer for BuildingFund model for managers'''
    class Meta:
        model = BuildingFund
        fields = [
            'id',
            'building',
            'balance',
            'updated_at',
        ]
        
class ShowDemandFromResidents(serializers.ModelSerializer):
    '''Serializer to show demand from residents'''
    class Meta:
        model = Debt
        fields = [
            'id',
            'amount_due',
        ]