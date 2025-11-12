from django.contrib import admin
from .models import Building, BuildingResident


# 🔹 این کلاس برای نمایش ساکنین هر ساختمان به صورت inline در صفحه Building
class BuildingResidentInline(admin.TabularInline):  # یا StackedInline برای ظاهر عمودی‌تر
    model = BuildingResident
    extra = 1  # چند ردیف خالی برای افزودن سریع ساکن جدید
    autocomplete_fields = ('resident', 'added_by')  # انتخاب راحت‌تر از بین کاربران
    readonly_fields = ('added_at',)  # تاریخ اضافه شدن فقط خواندنی باشد
    fields = ('resident', 'is_approved', 'added_by', 'added_at')  # ترتیب و نمایش فیلدها


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "manager",
        "units",
        "building_type",
        "use_type",
        "shaba_number",
        "is_active",
        "created_at",
    )

    list_filter = ("building_type", "use_type", "is_active", "created_at")
    search_fields = ("name", "manager__first_name", "manager__last_name", "shaba_number", "address")
    
    # 🔹 نمایش ساکنین داخل صفحه ساختمان
    inlines = [BuildingResidentInline]

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "image",
                "address",
                "building_type",
                "use_type",
                "units",
                "shaba_number",
                "manager",
                "is_active"
            )
        }),
        ("اطلاعات زمانی", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ("created_at",)


@admin.register(BuildingResident)
class BuildingResidentAdmin(admin.ModelAdmin):
    """نمایش مجزای ساکنین ساختمان‌ها در admin"""
    list_display = ("resident", "building", "is_approved", "added_by", "added_at")
    list_filter = ("is_approved", "building", "added_at")
    search_fields = ("resident__first_name", "resident__last_name", "building__name")
    autocomplete_fields = ("resident", "building", "added_by")
    readonly_fields = ("added_at",)
