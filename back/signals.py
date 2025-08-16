
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Utilisateur, Tenant, SystemPayment, SystemOrder

BIZ_NAME_PREFIX = _("Pièces Auto")
BIZ_NAME_SUFFIX = _("s.a.r.l")

@receiver(post_save, sender=Utilisateur)
def utilisateur_created_or_updated(sender, instance, created, **kwargs):
    if created:
        create_tenant = False
        if not instance.is_superuser:
            if not instance.created_by:
                create_tenant = True

        if create_tenant :
            biz_name = instance.last_name if instance.last_name else  instance.username
            biz_owner = f"{instance.first_name} {biz_name}" if instance.first_name else biz_name
            tenant = Tenant(
                name = f'{BIZ_NAME_PREFIX} {biz_name.title()} {BIZ_NAME_SUFFIX}',
                owner = biz_owner.title(),
                email = instance.email,
                # created_by_user = instance.username,
                created_by = instance
            )

            try:
                tenant.save()
                instance.tenant = tenant
                instance.is_tenant_admin = True
                instance.save()
            except Exception as xc:
                print(f'Error while creating Tenant: {str(xc)}')

# @receiver(post_delete, sender=Utilisateur)
# def utilisateur_deleted(sender, instance, **kwargs):
#     print(f"Object deleted: {instance}")


@receiver(post_save, sender=SystemPayment)
def s_payment_created_or_updated(sender, instance, created, **kwargs):
    if instance:
        instance.order.update_status()

@receiver(post_delete, sender=SystemPayment)
def s_payment_deleted(sender, instance, **kwargs):
    if instance:
        instance.order.update_status()


# @receiver(post_save, sender=SystemOrder)
# def s_order_created_or_updated(sender, instance, created, **kwargs):
#     if instance:
#         instance.update_status()

# @receiver(post_delete, sender=SystemOrder)
# def s_order_deleted(sender, instance, **kwargs):
#     if instance:
#         instance.update_status()