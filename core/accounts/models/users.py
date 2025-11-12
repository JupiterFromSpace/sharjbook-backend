from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Roles(models.TextChoices):
        MANAGER = 'MANAGER', 'مدیر ساختمان'
        RESIDENT = 'RESIDENT', 'ساکن'
        
    phone_validator = RegexValidator(
        regex=r'^\+98\d{10}$',
        message='شماره تماس باید با +98 شروع شود و 10 رقم بعد از آن بیاید. مثال: +989123456789'
    )
    
    
    role = models.CharField(max_length=20, choices=Roles.choices, verbose_name='نقش کاربر')
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    phone = models.CharField(validators=[phone_validator],max_length=13, verbose_name='شماره تماس')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت فعال")


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