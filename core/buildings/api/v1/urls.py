from django.urls import path
from .views import (
    CreateBuildingView,
    ShowBuildingsView,
    AddResidentView,
    ListResidentView,
    TransferDebtsView,
)

app_name = "api-v1"

urlpatterns = [
    path("create/", CreateBuildingView.as_view(), name="building-create"),
    path("my-buildings/", ShowBuildingsView.as_view(), name="my-buildings"),
    path(
        "add-resident/<uuid:building_id>/",
        AddResidentView.as_view(),
        name="add-resident",
    ),
    path(
        "my-residents/<uuid:building_id>/",
        ListResidentView.as_view(),
        name="my-residents",
    ),
    path(
        "residents/<uuid:resident_id>/transfer-debts/",
        TransferDebtsView.as_view(),
        name="transfer-debts",
    ),
]
