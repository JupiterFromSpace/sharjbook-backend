from django.urls import path

from .views import RequestOTPView, VerifyOTPView, RefreshTokenView, LogoutView, UpdateProfileView, EmailPasswordLoginView

app_name = "accounts"

urlpatterns = [
    path("request-otp/",       RequestOTPView.as_view(),        name="request_otp"),
    path("verify-otp/",        VerifyOTPView.as_view(),          name="verify_otp"),
    path("login/",             EmailPasswordLoginView.as_view(), name="email_login"),
    path("token/refresh/",     RefreshTokenView.as_view(),       name="token_refresh"),
    path("logout/",            LogoutView.as_view(),             name="logout"),
    path("get-update/profile/",UpdateProfileView.as_view(),      name="update_profile"),
]
