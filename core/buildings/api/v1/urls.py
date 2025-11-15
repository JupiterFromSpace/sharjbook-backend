from django.urls import path
from .views import CreateBuildingView, ShowBuildingsView

app_name = 'buildings'

urlpatterns = [
    path('create/', CreateBuildingView.as_view(), name='building-create'),
    path('my-buildings/', ShowBuildingsView.as_view(), name='my-buildings'),
]
