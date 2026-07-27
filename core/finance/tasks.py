from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from buildings.models import BuildingResident
from finance.models import Debt


@shared_task
def generate_monthly_debts():
    '''
    این تسک یک‌بار در ابتدای هر ماه، توسط Celery Beat به‌صورت خودکار اجرا می‌شود
    (خودمان صداش نمی‌زنیم، Beat طبق زمان‌بندیِ تعریف‌شده در settings.py صداش می‌زند).

    کارش: برای هر ساکنِ تاییدشده (BuildingResident که is_approved=True است)،
    یک بدهی (Debt) جدید به مبلغ شارژ ماهیانه‌ی همان ساکن (monthly_charge_amount)
    می‌سازد، با سررسید ۱۰ روز بعد از تاریخ صدور.

    اگر بدهیِ همین ماه برای همین واحد قبلاً ساخته شده باشد (مثلاً به‌خاطر اجرای
    تصادفیِ دوباره‌ی تسک)، دوباره ساخته نمی‌شود؛ یعنی این تسک idempotent است.
    '''
    today = timezone.now().date()
    month_title = f"شارژ {today.strftime('%Y/%m')}"

    residents = BuildingResident.objects.filter(
        is_approved=True
    ).select_related("building", "resident")

    created_count = 0

    for resident_relation in residents:
        already_exists = Debt.objects.filter(
            building=resident_relation.building,
            unit_number=resident_relation.unit,
            title=month_title,
        ).exists()

        if already_exists:
            continue

        Debt.objects.create(
            building=resident_relation.building,
            unit_number=resident_relation.unit,
            responsible=resident_relation.resident,
            title=month_title,
            amount_due=resident_relation.monthly_charge_amount,
            due_date=today + timedelta(days=10),
        )
        created_count += 1

    return f"{created_count} بدهی جدید ساخته شد"


@shared_task
def send_debt_issued_notification(debt_id):
    '''
    این تسک بلافاصله بعد از ساخته‌شدن یک Debt، توسط سیگنالِ post_save در
    finance/signals.py صدا زده می‌شود (نه به‌صورت مستقیم از یک view).

    کارش: بدهی را با آی‌دی‌اش پیدا می‌کند و اگر مسئولِ پرداختش (responsible)
    مشخص باشد، یک ایمیل اطلاع‌رسانی برایش می‌فرستد. اگر واحد فعلاً هیچ
    مسئولی نداشته باشد (مثلاً واحد خالی است)، بی‌سروصدا از ارسال صرف‌نظر
    می‌کند - چون این حالت خطا نیست، فقط یعنی فعلاً کسی برای اطلاع‌رسانی
    وجود ندارد.

    آی‌دی (نه خودِ آبجکت) به تسک پاس داده می‌شود، چون بین زمانی که سیگنال
    صدا زده می‌شود و زمانی که worker واقعاً تسک را اجرا می‌کند، ممکن است
    فاصله بیفتد؛ پاس دادن id و خواندن دوباره از دیتابیس مطمئن‌تر از پاس
    دادن خودِ instance است.
    '''
    try:
        debt = Debt.objects.select_related("responsible").get(id=debt_id)
    except Debt.DoesNotExist:
        return "بدهی مورد نظر یافت نشد (شاید در این فاصله حذف شده)"

    if debt.responsible is None or not debt.responsible.email:
        return "این بدهی مسئول پرداخت مشخصی با ایمیل ندارد، ایمیلی ارسال نشد"

    subject = f"بدهی جدید: {debt.title}"
    message = (
        f"یک بدهی جدید برای واحد {debt.unit_number} صادر شد.\n"
        f"عنوان: {debt.title}\n"
        f"مبلغ: {debt.amount_due} تومان\n"
        f"سررسید: {debt.due_date}\n"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [debt.responsible.email],
        fail_silently=False,
    )

    return f"اطلاع‌رسانی برای بدهی {debt.id} ارسال شد"