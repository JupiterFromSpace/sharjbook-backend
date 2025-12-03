from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("کاربر باید شماره موبایل داشته باشد.")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("سوپریوزر باید is_staff=True باشد")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("سوپریوزر باید is_superuser=True باشد")

        return self.create_user(phone, password, **extra_fields)



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    username = None 
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    class Roles(models.TextChoices):
        MANAGER = 'MANAGER', 'مدیر ساختمان'
        RESIDENT = 'RESIDENT', 'ساکن'
        
    phone_validator = RegexValidator(
        regex=r'^\+98\d{10}$',
        message='شماره تماس باید با +98 شروع شود و 10 رقم بعد از آن بیاید. مثال: +989123456789'
    )
    
    
    role = models.CharField(max_length=20, choices=Roles.choices, default="MANAGER", verbose_name='نقش کاربر')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام خانوادگی')
    phone = models.CharField(validators=[phone_validator],max_length=13, unique=True, verbose_name='شماره تماس')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت فعال")
    
    active_building = models.ForeignKey(
        'buildings.Building',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='active_users',
        verbose_name='ساختمان فعال کاربر'
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"
    
    @property
    def is_manager(self):
        return self.role == self.Roles.MANAGER
    
    @property
    def is_resident(self):
        return self.role == self.Roles.RESIDENT