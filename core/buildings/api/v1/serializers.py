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
            'address',
            'building_type',
            'use_type',
            'units',
            'shaba_number',
            'monthly_charge_amount',
            'balance',
        ]
        read_only_fields = ['id', 'balance']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
    
        validated_data['manager'] = user
        building = Building.objects.create(**validated_data)
    
        # 👇 اضافه کردن مدیر به ساکنین
        from buildings.models import BuildingResident
        BuildingResident.objects.create(
            building=building,
            resident=user,
            is_approved=True
        )
    
        return building


    def get_balance(self, obj):
        return obj.fund.balance if hasattr(obj, 'fund') else 0




class BuildingListSerializer(serializers.ModelSerializer):
    user_role = serializers.SerializerMethodField()
    
    class Meta:
        model = Building
        fields = [
            'id',
            'name',
            'address',
            'building_type',
            'use_type',
            'user_role',
        ]

    def get_user_role(self, obj):
        user = self.context["request"].user  

        if obj.manager_id == user.id:
            return 'MANAGER'

        if obj.building_residents.filter(resident=user, is_approved=True).exists():
            return 'RESIDENT'

        return 'NONE'


class SelectActiveBuildingSerializer(serializers.Serializer):
    building_id = serializers.UUIDField()

    def validate(self, attrs):
        user = self.context["request"].user
        building_id = attrs["building_id"]

        try:
            building = Building.objects.get(id=building_id)
        except Building.DoesNotExist:
            raise serializers.ValidationError("ساختمان یافت نشد.")

        if building.manager_id != user.id:
            raise serializers.ValidationError("شما مدیر این ساختمان نیستید.")

        attrs["building"] = building
        return attrs
