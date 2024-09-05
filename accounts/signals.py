from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import UserProfile 
from .utils import generate_default_avatar
from stock.models import Requester


    

@receiver(pre_save, sender=UserProfile)
def user_pre_save(sender, instance, **kwargs):
    if not instance.profile_image:
        default_avatar = generate_default_avatar(instance.user.get_username())
        instance.profile_image.save(
            'default_avatar.png', default_avatar, save=False)
        

@receiver(post_delete, sender=UserProfile)
def delete_avatar_user(sender, instance, **kwargas):
    if instance.profile_image:
        instance.profile_image.delete(False)


@receiver(post_save, sender=UserProfile)
def user_to_requester(sender, instance, **kargs):
    requester, created = Requester.objects.get_or_create(user=instance.user)

    requester.full_name = f"{instance.user.first_name} {instance.user.last_name}"
    requester.unit.set(instance.unit.all())
    requester.sector.set(instance.sector.all())
    requester.save()


@receiver(m2m_changed, sender=UserProfile.sector.through)
def update_requester_sector(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        try:
            requester = Requester.objects.get(user=instance.user)
            requester.sector.set(instance.sector.all())
            requester.save()
        except Requester.DoesNotExist:
            pass


        
@receiver(m2m_changed, sender=UserProfile.unit.through)
def update_requester_unit(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        try:
            requester = Requester.objects.get(user=instance.user)
            # Atualiza as unidades do Requisitante para refletir as mudanças no UserProfile
            requester.unit.set(instance.unit.all())
            requester.save()
        except Requester.DoesNotExist:
            pass