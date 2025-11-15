from rest_framework import serializers
from buildings.models import Building, BuildingResident
from finance.models import BuildingFund

class CreateBuildingSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Building
        fields = [
            'id',
            'name',
            'building_type',
            'use_type',
            'units',
            'shaba_number',
            'monthly_charge_amount',
            'balance',
        ]
        read_only_fields = ['id', 'balance']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['manager'] = user 

        building = Building.objects.create(**validated_data)
        BuildingFund.objects.create(building=building)
        return building


    def get_balance(self, obj):
        return obj.fund.balance if hasattr(obj, 'fund') else 0