from django.urls import path
from .views import CreateBuildingView

app_name = 'buildings'

urlpatterns = [
    path('create/', CreateBuildingView.as_view(), name='building-create'),
]
