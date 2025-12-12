from django.urls import path
from .views import (CreateBuildingView, ShowBuildingsView, SelectActiveBuildingView,
        AddResidentView                
    )

app_name = 'buildings'

urlpatterns = [
    path('create/', CreateBuildingView.as_view(), name='building-create'),
    path('my-buildings/', ShowBuildingsView.as_view(), name='my-buildings'),
    path('set-active-building/', SelectActiveBuildingView.as_view(), name='set-active-building'),
    path('add-resident/<uuid:building_id>/', AddResidentView.as_view(), name = 'add-resident'),
]
