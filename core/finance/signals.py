from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Payment, BuildingFund


@receiver(post_save, sender=Transaction)
def update_fund_on_transaction(sender, instance, created, **kwargs):
    """
    وقتی تراکنش جدید ساخته شد، صندوق ساختمان رو به‌روزرسانی کن
    """
    if created and instance.is_paid:
        fund, _ = BuildingFund.objects.get_or_create(building=instance.building)
        fund.apply_transaction(instance)


@receiver(post_save, sender=Payment)
def update_fund_on_payment(sender, instance, created, **kwargs):
    """
    وقتی پرداخت جدید انجام شد، مبلغ رو به صندوق اضافه کن
    """
    if created:
        fund, _ = BuildingFund.objects.get_or_create(building=instance.transaction.building)
        fund.balance += instance.amount_paid
        fund.save()
