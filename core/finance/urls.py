from django.urls import path, include

app_name = 'finance'

urlpatterns = [
    path('api/v1/',include('finance.api.v1.urls')),
]