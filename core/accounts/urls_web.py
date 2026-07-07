from django.urls import path
from .views_web import home_view, login_view, signup_view, logout_view

urlpatterns = [
    path("login/",  login_view,  name="web-login"),
    path("signup/", signup_view, name="web-signup"),
    path("logout/", logout_view, name="web-logout"),
]
