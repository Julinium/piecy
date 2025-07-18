import uuid #, os
from django.db import models
from django.utils.translation import gettext as _
from datetime import date, datetime


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True)
    verified = models.BooleanField(blank=True, null=True)
    username = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)

    created_by = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'user'


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=16, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    whatsapp = models.CharField(max_length=16, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    owner = models.CharField(max_length=64, blank=True, null=True)
    channel = models.CharField(max_length=32, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    # owned_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'tenant'


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    date_fm = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True)
    plan = models.ForeignKey('Plan', on_delete=models.RESTRICT, blank=True, null=True)
    payment = models.ForeignKey('SystemPayment', on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

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

    owned_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'system_payment'


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    header = models.CharField(max_length=128, blank=True, null=True)
    ordre = models.SmallIntegerField(blank=True, null=True)
    cta = models.CharField(max_length=128, blank=True, null=True, default=_('Free quote'))
    
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

    owned_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'plan'


class Registre(models.Model):
    OPERATIONS = [('C', 'Create'), ('R', 'Read'), ('U', 'Update'), ('D', 'Delete'),]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    date = models.DateField(blank=True, null=True)
    model = models.CharField(max_length=32, blank=True, null=True)
    instance = models.CharField(max_length=128, blank=True, null=True)
    operation = models.CharField(max_length=1, choices=OPERATIONS, default='C')

    owned_by = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'registre'