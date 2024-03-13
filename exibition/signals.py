from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.conf import settings
from .models import Owner


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_owner_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Owner.objects.create(user=kwargs['instance'])


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def delete_owner_for_deleted_user(sender, **kwargs):
    try:
        owner = Owner.objects.get(user=kwargs['instance'])
        owner.delete()
    except Owner.DoesNotExist:
        pass
