from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import LoginView, RefreshTokenView, LogoutView, UpdateProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('show/profile/', UpdateProfileView.as_view(), name='show_profile')
]
