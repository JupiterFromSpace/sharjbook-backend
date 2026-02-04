from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from buildings.models import Building
import uuid

User = settings.AUTH_USER_MODEL


class Transaction(models.Model):
    """
    تراکنش مالی واقعی ساختمان
    فقط زمانی ساخته می‌شود که پول واقعاً وارد یا خارج شود
    (درآمد یا هزینه)
    """

    class TransactionTypes(models.TextChoices):
        INCOME = "INCOME", "درآمد"
        EXPENSE = "EXPENSE", "هزینه"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="ساختمان",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_transactions",
        verbose_name="ایجاد کننده",
    )

    transaction_type = models.CharField(
        max_length=10, choices=TransactionTypes.choices, verbose_name="نوع تراکنش"
    )

    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="مبلغ (ریال)",
    )

    date = models.DateField(verbose_name="تاریخ تراکنش")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"

    def __str__(self):
        return f"{self.title} - {self.amount} ریال"


class Debt(models.Model):
    """
    بدهی‌های مالی مربوط به یک واحد
    شامل شارژ ماهانه یا هزینه خاص
    بدهی همیشه به نام "مسئول پرداخت" ثبت می‌شود
    اگر واحد خالی باشد، مالک واحد مسئول خواهد بود
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name="debts", verbose_name="ساختمان"
    )

    unit_number = models.PositiveIntegerField(verbose_name="شماره واحد")

    responsible = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="debts",
        verbose_name="مسئول پرداخت",
        null=True,  # NULL به جای default تا رکوردهای قدیمی درست migrate شوند
        blank=True,
    )

    title = models.CharField(max_length=200, verbose_name="عنوان بدهی")

    amount_due = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="مبلغ بدهی",
    )

    due_date = models.DateField(verbose_name="تاریخ سررسید")

    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده؟")

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["due_date"]
        verbose_name = "بدهی"
        verbose_name_plural = "بدهی‌ها"

    def __str__(self):
        return f"واحد {self.unit_number} - {self.amount_due} ریال"


class Payment(models.Model):
    """
    پرداختی که برای تسویه یک بدهی انجام می‌شود
    می‌تواند نقدی، بانکی یا آنلاین باشد
    """

    class Status(models.TextChoices):
        PENDING = "PENDING", "در انتظار"
        SUCCESS = "SUCCESS", "موفق"
        FAILED = "FAILED", "ناموفق"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    debt = models.ForeignKey(
        Debt,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="بدهی مربوطه",
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="تراکنش مالی",
    )

    paid_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="پرداخت کننده",
    )

    amount_paid = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="مبلغ پرداختی",
    )

    method = models.CharField(
        max_length=20,
        choices=[
            ("CASH", "نقدی"),
            ("BANK", "بانکی"),
            ("ONLINE", "آنلاین"),
        ],
        verbose_name="روش پرداخت",
    )

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )

    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-paid_at"]
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"{self.amount_paid} ریال - {self.get_status_display()}"


class BuildingFund(models.Model):
    """
    صندوق مالی ساختمان
    نگهدارنده موجودی واقعی ساختمان
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    building = models.OneToOneField(
        Building, on_delete=models.CASCADE, related_name="fund", verbose_name="ساختمان"
    )

    balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, verbose_name="موجودی (ریال)"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "صندوق ساختمان"
        verbose_name_plural = "صندوق‌های ساختمان"

    def apply_transaction(self, transaction):
        """
        اعمال تراکنش روی موجودی صندوق
        در صورتی که تراکنش درآمد باشد موجودی افزایش می‌یابد
        و اگر هزینه باشد موجودی کاهش می‌یابد
        """
        if transaction.transaction_type == Transaction.TransactionTypes.INCOME:
            self.balance += transaction.amount
        elif transaction.transaction_type == Transaction.TransactionTypes.EXPENSE:
            self.balance -= transaction.amount
        self.save()

    def __str__(self):
        return f"{self.building.name} - {self.balance} ریال"


class ZarinpalTransaction(models.Model):
    """
    اطلاعات پرداخت آنلاین از درگاه زرین‌پال
    """

    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name="zarinpal"
    )

    authority = models.CharField(max_length=255, unique=True)
    ref_id = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.authority
