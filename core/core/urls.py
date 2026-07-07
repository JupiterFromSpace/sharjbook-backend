"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from accounts.views_web import home_view

schema_view = get_schema_view(
    openapi.Info(
        title="ShargBook API",
        default_version="v1",
        description="سیستم مدیریت شارژ و امور مالی ساختمان",
        contact=openapi.Contact(email="sinamatari23@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("",        home_view, name="home"),
    path("admin/",  admin.site.urls),

    # مستندات API
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    # API endpoints
    path("accounts/", include("accounts.urls")),
    path("building/", include("buildings.urls")),
    path("finance/",  include("finance.urls")),

    # Template-based web views (login/signup/logout)
    path("accounts/web/", include("accounts.urls_web")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

