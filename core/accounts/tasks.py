from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_email(email, code):
    subject = "کد ورود به شارژبوک"

    message = (
        f"کد ورود شما: {code}\n"
        "این کد تا ۲ دقیقه دیگر معتبر است.\n"
        "اگر این درخواست را شما نداده‌اید، این ایمیل را نادیده بگیرید."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )