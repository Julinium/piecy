
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Utilisateur, Tenant

@receiver(post_save, sender=Utilisateur)
def utilisateur_created_or_updated(sender, instance, created, **kwargs):
    if created:
        create_tenant = False
        if instance.created_by:
            creator = Utilisateur.objects.filter(id=instance.created_by).first()
            if not creator.tenant: create_tenant = True
        else: create_tenant = True
        
        if create_tenant :
            biz_name = instance.last_name if instance.last_name else  instance.username 
            biz_owner = f"{instance.first_name} {biz_name}" if instance.first_name else biz_name
            tenant = Tenant(
                name = f'Pièces Auto {biz_name.title()}',
                owner = biz_owner.title(),
                email = instance.email,
                created_by_user = instance.username,
                created_by = instance.id
            )
            try:
                tenant.save()
                instance.tenant = tenant
                instance.is_tenant_admin = True
                instance.save()
            except Exception as xc:
                print(f'Error while creating Tenant: {str(xc)}')

@receiver(post_delete, sender=Utilisateur)
def utilisateur_deleted(sender, instance, **kwargs):
    print(f"Object deleted: {instance}")


# def create_tenant(utilisateur):
#     print(f" +++++++++++++++++++++ Creating Tenant for {utilisateur} (id={utilisateur.created_by})")
#     create_tenant = False
#     if utilisateur.created_by:
#         print(f"cccccccccccccccccccccccccccccccccccccccccccccc")
#         creator = Utilisateur.objects.filter(id=utilisateur.created_by).first()
#         if not creator.tenant: create_tenant = True
#     else: create_tenant = True
    
#     if create_tenant :
#         biz_name = utilisateur.last_name if utilisateur.last_name else  utilisateur.username 
#         tenant = Tenant(
#             name = f'Pièces Auto {biz_name.title()}',
#             owner = f'{utilisateur.first_name} {biz_name}',
#             email = utilisateur.email,
#             created_by_user = utilisateur.username,
#             created_by = utilisateur.id
#         )
#         try:
#             print(f" +++++++++++++++ Saving Tenant { tenant }")
#             tenant.save()
#             utilisateur.tenant = tenant
#         except Exception as xc:
#             print(f'Error while creating Tenant: {str(xc)}')