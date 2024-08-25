from django.dispatch import receiver
from django.db.models.signals import pre_save
from bot.models import Order
from datetime import datetime


@receiver(pre_save, sender=Order)
def update_approve_time(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Order.objects.get(id=instance.pk)
        if old_instance.status == Order.OrderStatus.PENDING and old_instance.status != instance.status:
            instance.accountant_approve_time = datetime.now()

        if old_instance.status == Order.OrderStatus.APPROVED_BY_ACCOUNTANT and old_instance.status != instance.status:
            instance.director_approve_time = datetime.now()

        if old_instance.status == Order.OrderStatus.APPROVED_BY_DIRECTOR and old_instance.status != instance.status:
            instance.storekeeper_approve_time = datetime.now()

            