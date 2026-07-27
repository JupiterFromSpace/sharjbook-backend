from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Payment, BuildingFund, Debt
from buildings.models import Building
from .tasks import send_debt_issued_notification


@receiver(post_save, sender=Transaction)
def update_fund_on_transaction(sender, instance, created, **kwargs):
    """
    وقتی تراکنش جدید ساخته شد، صندوق ساختمان رو به‌روزرسانی کن
    """
    if created:
        fund, _ = BuildingFund.objects.get_or_create(building=instance.building)
        fund.apply_transaction(instance)


@receiver(post_save, sender=Payment)
def handle_payment(sender, instance, created, **kwargs):
    if created and instance.status == Payment.Status.SUCCESS:
        debt = instance.debt
        debt.is_paid = True
        debt.save()


@receiver(post_save, sender=Building)
def create_building_fund(sender, instance, created, **kwargs):
    if created:
        BuildingFund.objects.get_or_create(building=instance)


@receiver(post_save, sender=Debt)
def notify_debt_issued(sender, instance, created, **kwargs):
    """
    وقتی یک بدهی جدید ساخته شد (از هر مسیری - چه generate_monthly_debts،
    چه یک endpoint دستی در آینده)، به ساکن مسئولِ آن اطلاع بده.
    """
    if created:
        send_debt_issued_notification.delay(instance.id)