from django.core.mail import send_mail
from django.conf import settings
from accounts.tasks import send_otp_email

def send_otp(email, code):
    send_otp_email.delay(email, code)
    subject = "کد ورود به شارژبوک"
    message = (
        f"کد ورود شما: {code}\n"
        "این کد تا ۲ دقیقه دیگر معتبر است.\n"
        "اگر این درخواست را شما نداده‌اید، این ایمیل را نادیده بگیرید."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
