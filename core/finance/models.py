from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from buildings.models import Building
import uuid

user = settings.AUTH_USER_MODEL

class Transaction (models.Model):
    """تراکنش مالی کلی: شامل درآمد، هزینه یا بدهی"""
    
    class TransactionTypes(models.TextChoices):
        INCOME = 'INCOME','درآمد'
        EXPENSE = 'EXPENSE', 'هزینه'
        DEBT = 'DEBT', 'بدهی'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='مدیر ساختمان'    
    )
    created_by = models.ForeignKey(
        user,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_transactions',
        verbose_name='ایجاد کننده'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionTypes.choices,
        verbose_name='نوع تراکنش'
    )
    
    title = models.CharField(max_length=200, verbose_name='عنوان تراکنش')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='مبلغ (ریال)')
    date = models.DateField(verbose_name='تاریخ تراکنش')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده؟')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")


    class Meta:
        verbose_name = 'تراکنش مالی'
        verbose_name_plural = 'تراکنش‌ها'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_transaction_type_display()}) - {self.amount} ریال"



class Payment(models.Model):
    """پرداخت‌های انجام‌شده توسط ساکنین (مرتبط با تراکنش بدهی یا شارژ)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='تراکنش مربوطه'
    )
    resident = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'RESIDENT'},
        related_name='payments',
        verbose_name='ساکن پرداخت‌کننده'
    )
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='مبلغ پرداختی')
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پرداخت')
    reference_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد پیگیری بانکی')
    method = models.CharField(
        max_length=50,
        choices=[
            ('CASH', 'نقدی'),
            ('BANK', 'واریز بانکی'),
            ('ONLINE', 'پرداخت آنلاین'),
        ],
        verbose_name='روش پرداخت'
    )

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
        ordering = ['-paid_at']

    def __str__(self):
        return f"{self.resident.full_name} - {self.amount_paid} ریال"


class Debt(models.Model):
    """بدهی‌های باز هر ساکن (شارژ یا هزینه‌ای که هنوز نداده)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='debts',
        verbose_name='ساختمان'
    )
    resident = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'RESIDENT'},
        related_name='debts',
        verbose_name='ساکن بدهکار'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان بدهی')
    amount_due = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='مبلغ بدهی'
    )
    due_date = models.DateField(verbose_name='تاریخ سررسید')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده؟')

    class Meta:
        verbose_name = 'بدهی'
        verbose_name_plural = 'بدهی‌ها'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.resident.full_name} - {self.amount_due} ریال"



class BuildingFund(models.Model):
    """
    صندوق مالی هر ساختمان (نگهدارنده موجودی)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building = models.OneToOneField(
        Building,
        on_delete=models.CASCADE,
        related_name='fund',
        verbose_name='ساختمان'
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name='موجودی صندوق (ریال)'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')

    class Meta:
        verbose_name = 'صندوق ساختمان'
        verbose_name_plural = 'صندوق‌های ساختمان'

    def __str__(self):
        return f"صندوق {self.building.name} - موجودی: {self.balance} ریال"

    def apply_transaction(self, transaction):
        """
        اعمال تراکنش روی صندوق
        در صورتی که تراکنش درآمد باشد، موجودی افزایش می‌یابد
        و در صورت هزینه، موجودی کاهش می‌یابد.
        """
        if transaction.transaction_type == Transaction.TransactionTypes.INCOME:
            self.balance += transaction.amount
        elif transaction.transaction_type == Transaction.TransactionTypes.EXPENSE:
            self.balance -= transaction.amount
        self.save()

    def create_initial_fund(self):
        """ایجاد صندوق اولیه با موجودی صفر"""
        self.balance = 0
        self.save()