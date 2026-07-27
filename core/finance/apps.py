from django.apps import AppConfig


class FinanceConfig(AppConfig):
    '''
    تنظیمات اپ finance.

    متد ready() توسط خود Django موقع بالا آمدن پروژه صدا زده می‌شود
    (یک‌بار، بعد از این‌که همه‌ی مدل‌ها لود شدند). اینجا signals.py را
    import می‌کنیم تا @receiver هایی که آنجا تعریف شده‌اند واقعاً به
    سیگنال post_save وصل شوند. بدون این import، فایل signals.py هیچ‌وقت
    اجرا نمی‌شود و هیچ‌کدام از receiver ها فعال نمی‌شوند.
    '''
    default_auto_field = "django.db.models.BigAutoField"
    name = "finance"

    def ready(self):
        import finance.signals