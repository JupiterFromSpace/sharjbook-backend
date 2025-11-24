from django.urls import path
from .views import LoginView

app_name = 'buildings'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login')
]
