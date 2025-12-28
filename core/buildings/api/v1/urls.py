from django.urls import path
from .views import (CreateBuildingView, ShowBuildingsView,
        AddResidentView, ListResidentView                
    )

app_name = 'buildings'

urlpatterns = [
    path('create/', CreateBuildingView.as_view(), name='building-create'),
    path('my-buildings/', ShowBuildingsView.as_view(), name='my-buildings'),
    path('add-resident/<uuid:building_id>/', AddResidentView.as_view(), name = 'add-resident'),
    path('my-residents/<uuid:building_id>/', ListResidentView.as_view(), name='my-residents')
]
