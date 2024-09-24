from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CashOutflow, CashInflow, BankAccount


@receiver(post_save, sender=CashOutflow)
def update_bank_account_value(sender, instance, created, **kwargs):
    if instance.payment_date !=None:
        account = BankAccount.objects.get(id=instance.bank_account.id)
        account.value -= instance.total_value
        account.save() 

@receiver(post_save, sender=CashInflow)
def update_bank_account_value(sender, instance, created, **kwargs):
    if instance.payment_date !=None:
        account = BankAccount.objects.get(id=instance.bank_account.id)
        account.value += instance.total_value
        account.save() 