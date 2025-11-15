from django.urls import path, include

app_name = 'buildings'

urlpatterns = [
    path('api/v1/',include('buildings.api.v1.urls')),
]