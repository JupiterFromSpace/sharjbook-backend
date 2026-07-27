from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from buildings.models import BuildingResident


@shared_task
def send_join_request_notification(resident_relation_id):
    '''
    این تسک بلافاصله بعد از ثبتِ یک درخواست عضویت جدید (BuildingResident با
    is_approved=False)، توسط سیگنالِ post_save در buildings/signals.py صدا
    زده می‌شود.

    کارش: رابطه‌ی ساختمان/ساکن را با آی‌دی‌اش پیدا می‌کند و به ایمیل مدیر
    همان ساختمان اطلاع می‌دهد که یک درخواست عضویت جدید در انتظار تایید
    اوست.
    '''
    try:
        resident_relation = BuildingResident.objects.select_related(
            "building", "building__manager", "resident"
        ).get(id=resident_relation_id)
    except BuildingResident.DoesNotExist:
        return "رابطه‌ی ساکن مورد نظر یافت نشد (شاید در این فاصله حذف شده)"

    manager = resident_relation.building.manager

    if not manager.email:
        return "مدیر این ساختمان ایمیل ثبت‌شده‌ای ندارد، ایمیلی ارسال نشد"

    subject = f"درخواست عضویت جدید در {resident_relation.building.name}"
    message = (
        f"یک درخواست عضویت جدید برای واحد {resident_relation.unit} "
        f"در ساختمان «{resident_relation.building.name}» ثبت شده است.\n"
        "برای تایید یا رد آن به پنل مدیریت مراجعه کنید."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [manager.email],
        fail_silently=False,
    )

    return f"اطلاع‌رسانی برای درخواست عضویت {resident_relation.id} به مدیر ارسال شد"