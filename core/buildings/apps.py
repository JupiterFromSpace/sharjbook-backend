from django.apps import AppConfig


class BuildingsConfig(AppConfig):
    '''
    تنظیمات اپ buildings.

    مثل finance/apps.py، اینجا هم signals.py را در ready() ایمپورت می‌کنیم
    تا receiver هایش (اطلاع‌رسانی به مدیر هنگام درخواست عضویت جدید) واقعاً
    به سیگنال post_save وصل شوند.
    '''
    default_auto_field = "django.db.models.BigAutoField"
    name = "buildings"

    def ready(self):
        import buildings.signals