from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BuildingResident
from .tasks import send_join_request_notification


@receiver(post_save, sender=BuildingResident)
def notify_manager_of_join_request(sender, instance, created, **kwargs):
    """
    وقتی یک رابطه‌ی ساختمان/ساکن تازه ساخته شد و هنوز تایید نشده
    (is_approved=False)، یعنی این یک درخواست عضویتِ خودسرویس است (نه
    اضافه‌شدن دستی توسط مدیر که مستقیماً is_approved=True می‌سازد).
    در این حالت به مدیر ساختمان اطلاع بده.
    """
    if created and not instance.is_approved:
        send_join_request_notification.delay(instance.id)