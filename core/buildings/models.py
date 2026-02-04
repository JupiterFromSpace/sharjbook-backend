from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
import uuid

user = settings.AUTH_USER_MODEL


class Building(models.Model):

    class BuildingTypes(models.TextChoices):
        Building = "Building", "ساختمان"
        Block = "Block", "بلوک"
        Complex = "Complex", "مجتمع"
        Tower = "Tower", "برج"
        Town = "Town", "شهرک"

    class BuildingUseTypes(models.TextChoices):
        Residential = "Residential", "مسکونی"
        Office = "Office", "اداری"
        Commercial = "Commercial", "تجاری"
        Medical = "Medical", "پزشکی"
        Educational = "Educational", "آموزشی"
        Villa = "Villa", "ویلا"

    def building_image_upload_path(instance, filename):
        # Organize images by building ID
        return f"buildings/{instance.id}/images/{filename}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.TextField(verbose_name="آدرس ساختمان")
    name = models.CharField(max_length=300, verbose_name="نام ساختمان")
    image = models.ImageField(
        upload_to=building_image_upload_path,
        null=True,
        blank=True,
        verbose_name="عکس از ساختمان ",
    )
    building_type = models.CharField(
        max_length=20, choices=BuildingTypes.choices, verbose_name="نوع ساختمان"
    )
    use_type = models.CharField(
        max_length=20, choices=BuildingUseTypes.choices, verbose_name="کاربری ساختمان"
    )

    manager = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name="managed_buildings",
        limit_choices_to={"role": "MANAGER"},
        verbose_name="مدیر ساختمان",
    )

    residents = models.ManyToManyField(
        user,
        through="BuildingResident",
        through_fields=("building", "resident"),
        related_name="residential_buildings",
        blank=True,
        verbose_name="ساکنین",
    )

    units = models.PositiveIntegerField(verbose_name="تعداد واحدها")

    shaba_validator = RegexValidator(
        regex=r"^IR\d{24}$",
        message="شماره شبا باید با IR شروع شده و 24 رقم داشته باشد. مثال: IR123456789012345678901234",
    )
    shaba_number = models.CharField(
        max_length=26, validators=[shaba_validator], verbose_name="شماره شبا"
    )

    monthly_charge_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="مبلغ شارژ ماهیانه (ریال)",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت فعال")

    class Meta:
        verbose_name = "ساختمان"
        verbose_name_plural = "ساختمان‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.manager.full_name}"


class BuildingResident(models.Model):
    """مدل واسط بین ساختمان و ساکنین با جزئیات بیشتر"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="building_residents",
        verbose_name="ساختمان",
    )
    resident = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "RESIDENT"},
        related_name="residences",
        verbose_name="ساکن",
    )

    monthly_charge_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, verbose_name="شارژ ماهیانه واحد"
    )

    unit = models.PositiveIntegerField(verbose_name="واحد")

    added_by = models.ForeignKey(
        user,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_residents",
        verbose_name="افزوده شده توسط",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ اضافه شدن")
    is_approved = models.BooleanField(default=False, verbose_name="تأیید مدیر")

    class Meta:
        unique_together = ("building", "resident")
        verbose_name = "ساکن ساختمان"
        verbose_name_plural = "ساکنین ساختمان"

    def __str__(self):
        return f"{self.resident.full_name} در {self.building.name}"
