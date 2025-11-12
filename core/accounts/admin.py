from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("اطلاعات اضافی", {
            "fields": ("role", "phone"),
        }),
    )
    list_display = ("id","first_name","last_name", "email", "phone", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("id","first_name","last_name", "email", "phone")
