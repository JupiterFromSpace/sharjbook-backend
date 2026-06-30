from rest_framework import serializers
from finance.models import BuildingFund, Debt, Transaction


class ListBuildingFundSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source="building.name", read_only=True)

    class Meta:
        model = BuildingFund
        fields = ["id", "building", "building_name", "balance", "updated_at"]


class ShowDemandFromResidentsSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source="building.name", read_only=True)

    class Meta:
        model = Debt
        fields = ["id", "building", "building_name", "amount_due"]


class ShowDebtorsListSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source="responsible.full_name", read_only=True)
    building_name = serializers.CharField(source="building.name", read_only=True)

    class Meta:
        model = Debt
        fields = [
            "id",
            "building",
            "building_name",
            "responsible",
            "resident_name",
            "amount_due",
            "due_date",
            "is_paid",
        ]


class TransactionListSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source="building.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "building",
            "building_name",
            "transaction_type",
            "title",
            "description",
            "amount",
            "date",
            "created_at",
        ]
