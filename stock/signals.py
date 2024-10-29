from django.dispatch import receiver
from django.db import transaction
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete
from django.utils import timezone
from .models import (Unit, Requester, Item, Inflow, Outflow, Request, Inventory, Request)
from accounts.models import UserProfile


@receiver(post_save, sender=Inflow)
def post_save_inflows(sender, instance, **kwargs):
    update_inventory()


@receiver(post_delete, sender=Inflow)
def post_delete_inflows(sender, instance, **kwargs):
    update_inventory()


@receiver(post_save, sender=Outflow)
def post_save_outflow(sender, instance, **kwargs):
    update_inventory()


@receiver(post_delete, sender=Outflow)
def post_delete_outflows(sender, instance, **kwargs):
    update_inventory()



@receiver(post_save, sender=Request)
def create_outflow(sender, instance, created, **kwargs):
    if instance.status == 'Aprovado' and instance.delivery_status == 'Efetuada':
       for request_item in instance.request_item_request.all():
           Outflow.objects.create(
                item = request_item.item,
                date = timezone.now().date(),
                sector = instance.sector,
                requester = instance.requester,
                quantity = request_item.quantity,
                source_stock = instance.unit, 
                target_stock = instance.unit,
           )




def update_inventory():
    for item in Item.objects.all():
        for unit in Unit.objects.all():
            # Soma as quantidades de entrada (Inflow) para o item e unidade específicos
            total_inflow = Inflow.objects.filter(item=item, target_stock=unit).aggregate(
                total=Sum('quantity'))['total'] or 0
            
            # Soma as quantidades de saída (Outflow) para o item e unidade específicos
            total_outflow = Outflow.objects.filter(item=item, source_stock=unit).aggregate(
                total=Sum('quantity'))['total'] or 0
            
            # Calcula a quantidade total disponível no estoque
            total_quantity = total_inflow - total_outflow
            total_quantity = max(total_quantity, 0)  # Garante que não tenha quantidade negativa
            
            # Atualiza ou cria o inventário com a quantidade calculada
            if total_inflow > 0 or total_outflow > 0:
                Inventory.objects.update_or_create(
                    item=item,
                    unit=unit,
                    defaults={'quantity_available': total_quantity}
                )
            else:
                # Se não houver inflow e outflow, pode-se optar por remover o inventário correspondente
                Inventory.objects.filter(item=item, unit=unit).delete()


@receiver(m2m_changed, sender=Requester.sector.through)
def update_requester_sector(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        try:
            user = UserProfile.objects.get(user=instance.user)
            user.sector.set(instance.sector.all())
            user.save()
        except UserProfile.DoesNotExist:
            pass


@receiver(m2m_changed, sender=Requester.unit.through)
def update_requester_unit(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        try:
            user = UserProfile.objects.get(user=instance.user)
            user.unit.set(instance.unit.all())
            user.save()
        except UserProfile.DoesNotExist:
            pass


@receiver(pre_delete, sender=Requester)
def update_requester_delete(sender, instance, **kwargs):
    # Usar uma transação para garantir a atomicidade das operações
    with transaction.atomic():
        outflows = Outflow.objects.filter(requester=instance)
        purchases = Request.objects.filter(requester=instance)
        requests = Request.objects.filter(requester=instance)
        
        for i in outflows:
            try:
                i.requester_name = instance.full_name
                i.save()
            except ValueError as e:
                print(f"Erro ao atualizar Saida: {e}")
                # Se necessário, você pode definir outra ação aqui, como excluir a saída ou ignorá-la

        for j in purchases:
            try:
                j.requester_name = instance.full_name
                j.save()
            except ValueError as e:
                print(f"Erro ao atualizar OrdemDeCompra: {e}")
        
        for k in requests:
            try:
                k.requester_name = instance.full_name
                k.save()
            except ValueError as e:
                print(f"Erro ao atualizar RequisicaoSetor: {e}")


@receiver(post_save, sender=Outflow)
def stock_transfer(sender, instance, created, **kwargs):

    if instance.target_stock is not None and instance.target_stock != instance.source_stock:
        if created:
                Inflow.objects.create(
                    outflow=instance,
                    date=instance.date,
                    item=instance.item,
                    invoice='0000',
                    source_stock=instance.source_stock,
                    target_stock=instance.target_stock,
                    unit_cost=0,
                    quantity=instance.quantity,
                    total_cost=0,
                    observation='Transferência de Estoque',
                )
        else:

            previous = getattr(instance, '_pre_save_instance', None)
            if previous:
                important_camps = ['date', 'target_stock', 'source_stock','quantity', 'item']
                changed_camps = any(getattr(instance, camp) != getattr(previous, camp) for camp in important_camps )

                if changed_camps:
                    try:
                        inflow = instance.inflow
                        inflow.data = instance.data
                        inflow.item = instance.item
                        inflow.source_stock = instance.source_stock
                        inflow.target_stock = instance.target_stock
                        inflow.quantity = instance.quantity
                        inflow.save()
                    except Inflow.DoesNotExist:
                            Inflow.objects.create(
                                outflow=instance,
                                date=instance.date,
                                item=instance.item,
                                invoice='0000',
                                source_stock=instance.source_stock,
                                target_stock=instance.target_stock,
                                unit_cost=0,
                                quantity=instance.quantity,
                                total_cost=0,
                                observation='Transferência de Estoque',
                            )