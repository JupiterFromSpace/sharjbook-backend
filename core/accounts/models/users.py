from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta
import random
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("کاربر باید ایمیل داشته باشد.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("سوپریوزر باید is_staff=True باشد")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("سوپریوزر باید is_superuser=True باشد")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Roles(models.TextChoices):
        MANAGER = "MANAGER", "مدیر ساختمان"
        RESIDENT = "RESIDENT", "ساکن"

    phone_validator = RegexValidator(
        regex=r"^\+98\d{10}$",
        message="شماره تماس باید با +98 شروع شود و 10 رقم بعد از آن بیاید. مثال: +989123456789",
    )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default="",
        verbose_name="نقش کاربر",
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="ایمیل",
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        verbose_name="شماره تماس",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت فعال")

    active_building = models.ForeignKey(
        "buildings.Building",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="active_users",
        verbose_name="ساختمان فعال کاربر",
    )

    def __str__(self):
        return self.email or str(self.id)

    @property
    def full_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.email

    @property
    def is_manager(self):
        return self.role == self.Roles.MANAGER

    @property
    def is_resident(self):
        return self.role == self.Roles.RESIDENT


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.phone} - {self.code}"

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=2)
        return timezone.now() > expiration_time

    @staticmethod
    def generate_code():
        return f"{random.randint(100000, 999999)}"
