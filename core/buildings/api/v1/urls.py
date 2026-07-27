from django.urls import path
from .views import (
    CreateBuildingView,
    ShowBuildingsView,
    AddResidentView,
    ListResidentView,
    TransferDebtsView,
    JoinBuildingRequestView,
    PendingResidentsView,
    ApproveResidentView,
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
    path(
        "join/<uuid:building_id>/",
        JoinBuildingRequestView.as_view(),
        name="join-building",
    ),
    path(
        "<uuid:building_id>/pending-residents/",
        PendingResidentsView.as_view(),
        name="pending-residents",
    ),
    path(
        "pending-residents/<uuid:resident_id>/approve/",
        ApproveResidentView.as_view(),
        name="approve-resident",
    ),
]