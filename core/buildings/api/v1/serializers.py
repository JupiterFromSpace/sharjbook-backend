from rest_framework import serializers
from buildings.models import Building
from django.contrib.auth import get_user_model
from finance.models import BuildingFund

User = get_user_model()

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

        user = User.objects.get(username="user1")

        # کاربر درخواست‌دهنده → مدیر ساختمان شود
        validated_data['manager'] = user

        building = Building.objects.create(**validated_data)

        # ساخت صندوق ساختمان
        BuildingFund.objects.create(building=building)

        return building

    def get_balance(self, obj):
        return obj.fund.balance if hasattr(obj, 'fund') else 0



class BuildingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = [
            'id',
            'name',
            'address',
            'building_type',
            'use_type',
        ]
