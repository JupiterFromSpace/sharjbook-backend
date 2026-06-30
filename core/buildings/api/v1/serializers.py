from rest_framework import serializers
from buildings.models import Building
from finance.models import Transaction
from buildings.models import BuildingResident
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class CreateBuildingSerializer(serializers.ModelSerializer):
    """
    ایجاد ساختمان + ثبت مدیر به عنوان اولین ساکن
    همراه با اعتبارسنجی شماره واحد
    """

    balance = serializers.SerializerMethodField(read_only=True)

    # فقط برای ورودی
    initial_balance = serializers.DecimalField(
        max_digits=15, decimal_places=2, write_only=True, required=True
    )

    # متعلق به BuildingResident
    unit = serializers.IntegerField(
        write_only=True, required=True, help_text="شماره واحد مدیر ساختمان"
    )

    class Meta:
        model = Building
        fields = [
            "id",
            "name",
            "address",
            "building_type",
            "use_type",
            "units",
            "shaba_number",
            "monthly_charge_amount",
            "unit",
            "initial_balance",
            "balance",
        ]
        read_only_fields = ["id", "balance"]

    def validate(self, attrs):
        total_units = attrs.get("units")
        unit_number = attrs.get("unit")

        if unit_number < 1:
            raise serializers.ValidationError(
                {"unit": "شماره واحد باید عددی بزرگ‌تر از صفر باشد."}
            )

        if unit_number > total_units:
            raise serializers.ValidationError(
                {"unit": "شماره واحد نمی‌تواند بیشتر از تعداد کل واحدهای ساختمان باشد."}
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        unit = validated_data.pop("unit")
        initial_balance = validated_data.pop("initial_balance")

        # ایجاد ساختمان
        building = Building.objects.create(manager=user, **validated_data)

        # ثبت مدیر به عنوان اولین ساکن
        BuildingResident.objects.create(
            building=building,
            resident=user,
            unit=unit,
            added_by=user,
            is_approved=True,
            monthly_charge_amount=building.monthly_charge_amount,
        )

        # موجودی اولیه صندوق
        if initial_balance > 0:
            Transaction.objects.create(
                building=building,
                created_by=user,
                transaction_type=Transaction.TransactionTypes.INCOME,
                title="موجودی اولیه صندوق",
                amount=initial_balance,
                date=timezone.now().date(),
            )

        return building

    def get_balance(self, obj):
        return obj.fund.balance if hasattr(obj, "fund") else 0


class BuildingListSerializer(serializers.ModelSerializer):
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = [
            "id",
            "name",
            "address",
            "building_type",
            "use_type",
            "user_role",
        ]

    def get_user_role(self, obj):
        user_id = self.context["request"].user.id

        # مدیر ساختمان
        if obj.manager_id == user_id:
            return "MANAGER"

        # ساکن تایید شده (بدون query جدید)
        for br in obj.building_residents.all():
            if br.resident_id == user_id and br.is_approved:
                return "RESIDENT"

        return "NONE"


class AddResidentSerializer(serializers.Serializer):
    full_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True, validators=[User.phone_validator])
    unit = serializers.IntegerField(write_only=True)
    monthly_charge_amount = serializers.DecimalField(
        max_digits=15, decimal_places=2, write_only=True
    )

    def validate(self, attrs):
        phone = attrs["phone"]
        building = self.context["building"]

        user = User.objects.filter(phone=phone).first()

        if (
            user
            and BuildingResident.objects.filter(
                building=building, resident=user
            ).exists()
        ):
            raise serializers.ValidationError(
                {"phone": "این ساکن قبلاً در این ساختمان ثبت شده است."}
            )

        if attrs["unit"] > building.units:
            raise serializers.ValidationError({"unit": "شماره واحد معتبر نیست."})

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
            },
        )

        if BuildingResident.objects.filter(building=building, resident=user).exists():
            raise serializers.ValidationError(
                "این ساکن قبلاً در این ساختمان ثبت شده است."
            )

        return BuildingResident.objects.create(
            building=building,
            resident=user,
            unit=unit,
            monthly_charge_amount=monthly_charge_amount,
            added_by=request.user,
            is_approved=True,
        )


class ListResidentSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="resident.phone", read_only=True)
    full_name = serializers.CharField(source="resident.full_name", read_only=True)

    class Meta:
        model = BuildingResident
        fields = [
            "unit",
            "full_name",
            "phone",
            "monthly_charge_amount",
        ]


class ResidentTransferSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    phone = serializers.CharField(max_length=13, required=False)

    def validate_phone(self, value):
        if value and not value.startswith("+98"):
            raise serializers.ValidationError("شماره تماس باید با +98 شروع شود")
        return value
