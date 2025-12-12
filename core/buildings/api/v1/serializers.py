from rest_framework import serializers
from django.db import transaction
from buildings.models import Building
from django.contrib.auth import get_user_model
from buildings.models import BuildingResident

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



class AddResidentSerializer(serializers.Serializer):
    full_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    unit = serializers.IntegerField(write_only=True)
    monthly_charge_amount = serializers.DecimalField(
        max_digits=15, decimal_places=2, write_only=True
    )

    def validate(self, attrs):
        phone = attrs["phone"]
        building = self.context["building"]

        if User.objects.filter(
            phone=phone,
            residential_buildings=building
        ).exists():
            raise serializers.ValidationError("این کاربر قبلاً در این ساختمان ثبت شده است.")

        if attrs["unit"] > building.units:
            raise serializers.ValidationError("شماره واحد معتبر نیست.")

        return attrs

    def create(self, validated_data):
        building = self.context["building"]
        request = self.context["request"]

        phone = validated_data["phone"]
        full_name = validated_data["full_name"]
        unit = validated_data["unit"]
        monthly_charge_amount = validated_data["monthly_charge_amount"]

        parts = full_name.strip().split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                "role": User.Roles.RESIDENT,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        if not created and user.role != User.Roles.RESIDENT:
            user.role = User.Roles.RESIDENT
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        resident = BuildingResident.objects.create(
            building=building,
            resident=user,
            unit=unit,
            monthly_charge_amount=monthly_charge_amount,
            added_by=request.user,
            is_approved=True
        )

        return resident
