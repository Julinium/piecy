import uuid #, os
from django.db import models
# from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
# from accs.models import Utilisateur as User

# User = get_user_model()


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    whatsapp = models.CharField(max_length=16, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    logo = models.ImageField(verbose_name=_("Logo"), upload_to='tenants/logos/', blank=True, null=True)
    brand = models.ImageField(verbose_name=_("Bannière"), upload_to='tenants/brands/', blank=True, null=True)
    header = models.ImageField(verbose_name=_("En-tête"), upload_to='tenants/headers/', blank=True, null=True)
    footer = models.ImageField(verbose_name=_("Bas de page"), upload_to='tenants/footers/', blank=True, null=True)
    owner = models.CharField(max_length=64, blank=True, null=True)
    channel = models.CharField(max_length=32, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    # owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    # created_by = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)
    # edited_by = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'tenant'
    
    def __str__(self):
        return f'{self.name} - {self.owner}'


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    date_fm = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True)
    plan = models.ForeignKey('Plan', on_delete=models.RESTRICT, blank=True, null=True)
    payment = models.ForeignKey('SystemPayment', on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'subscription'


class SystemPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    verified = models.BooleanField(blank=True, null=True)
    reference = models.CharField(max_length=32, blank=True, null=True)
    mode = models.CharField(max_length=32, blank=True, null=True)
    date_made = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=16, blank=True, null=True)
    maker = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=64, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'system_payment'


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    header = models.CharField(max_length=128, blank=True, null=True)
    ordre = models.SmallIntegerField(blank=True, null=True)
    # cta = models.CharField(max_length=128, blank=True, null=True, default=_('Free quote'))
    
    year_free_mth = models.SmallIntegerField(blank=True, null=True, default=2)
    first_time_disc = models.SmallIntegerField(blank=True, null=True, default=50)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)

    custom_domain = models.BooleanField(blank=True, null=True)
    mailbox = models.BooleanField(blank=True, null=True)
    ecommerce = models.BooleanField(blank=True, null=True)
    vitrine = models.BooleanField(blank=True, null=True)

    max_users = models.SmallIntegerField(blank=True, null=True)
    max_clients = models.SmallIntegerField(blank=True, null=True)
    max_products = models.SmallIntegerField(blank=True, null=True)
    max_pdfs = models.SmallIntegerField(blank=True, null=True)
    max_excels = models.SmallIntegerField(blank=True, null=True)

    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'plan'
    
    def __str__(self):
        return f'{self.name}'


class Registre(models.Model):
    OPERATIONS = [('C', 'Create'), ('R', 'Read'), ('U', 'Update'), ('D', 'Delete'),]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    date = models.DateField(blank=True, null=True)
    model = models.CharField(max_length=32, blank=True, null=True)
    instance = models.CharField(max_length=128, blank=True, null=True)
    operation = models.CharField(max_length=1, choices=OPERATIONS, default='C')

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'registre'