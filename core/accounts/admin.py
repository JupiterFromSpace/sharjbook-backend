from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models.users import User, OTP
from .models.profiles import Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    # چون username نداریم، باید ordering را تغییر دهیم
    ordering = ("phone",)

    # فیلدهایی که در لیست نمایش داده می‌شود
    list_display = ("id", "first_name", "last_name", "phone", "role", "is_active")

    # فیلترهای سایدبار
    list_filter = ("role", "is_active")

    # فیلدهای قابل جستجو
    search_fields = ("first_name", "last_name", "phone")

    # بازنویسی کامل fieldsets
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("اطلاعات شخصی", {"fields": ("first_name", "last_name")}),
        (
            "نقش و دسترسی‌ها",
            {"fields": ("role", "is_active", "is_staff", "is_superuser")},
        ),
        ("تاریخ‌ها", {"fields": ("last_login", "date_joined")}),
    )

    # فرم ساخت کاربر جدید در admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2", "role"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "first_name", "last_name", "created_date")
    search_fields = ("user__phone", "first_name", "last_name")
    ordering = ("-created_date",)


# ----------------------------
# OTP admin (فقط readonly)
# ----------------------------


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "is_used", "created_at", "expired_status")
    readonly_fields = ("user", "code", "is_used", "created_at")

    def expired_status(self, obj):
        return "منقضی شده" if obj.is_expired() else "فعال"

    expired_status.short_description = "وضعیت انقضا"
    expired_status.admin_order_field = "created_at"
