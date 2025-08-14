import uuid #, os
from django.db import models
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.utils.translation import gettext as _

# from django.conf import settings
# from django.db import models
# from decimal import Decimal

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(verbose_name=_("Activé"), blank=True, null=True, default=True)
    onboarded = models.BooleanField(verbose_name=_("Onboarded"), blank=True, null=True, default=False)
    # can_try = models.BooleanField(verbose_name=_("Peut tester"), blank=True, null=True, default=True)
    name = models.CharField(verbose_name=_("Nom"), max_length=128, blank=True, null=True)

    email = models.CharField(verbose_name=_("Email"), max_length=128, blank=True, null=True)
    phone = models.CharField(verbose_name=_("Tél."), max_length=16, blank=True, null=True)
    whatsapp = models.CharField(verbose_name=_("Whatsapp"), max_length=16, blank=True, null=True)

    address1 = models.CharField(verbose_name=_("Adresse ligne 1"), max_length=64, blank=True, null=True, default="N°24, Rue La Fontaine")
    address2 = models.CharField(verbose_name=_("Adresse ligne 2"), max_length=64, blank=True, null=True, default="Av. Mohammed V, Quartier Massira")
    city = models.CharField(verbose_name=_("Ville"), max_length=64, blank=True, null=True, default="Rabat")
    zip_code = models.CharField(verbose_name=_("Code postal"), max_length=64, blank=True, null=True, default="10000")
    state = models.CharField(verbose_name=_("Région ou état"), max_length=64, blank=True, null=True, default="Région Rabat-Salé-Kenitra")
    country = models.CharField(verbose_name=_("Pays"), max_length=64, blank=True, null=True, default=_('Maroc'))

    domain_name = models.CharField(verbose_name=_("Nom de domaine"), max_length=32, blank=True, null=True, default="mode-777.com")
    # slug = models.CharField(verbose_name=_("Nom abrégé"), max_length=32, blank=True, null=True)
    logo = models.ImageField(verbose_name=_("Logo"), upload_to='tenants/logos/', blank=True, null=True)
    brand = models.ImageField(verbose_name=_("Bannière"), upload_to='tenants/brands/', blank=True, null=True)
    header = models.ImageField(verbose_name=_("En-tête"), upload_to='tenants/headers/', blank=True, null=True)
    footer = models.ImageField(verbose_name=_("Bas de page"), upload_to='tenants/footers/', blank=True, null=True)
    owner = models.CharField(verbose_name=_("Propriétaire"), max_length=64, blank=True, null=True)
    channel = models.CharField(verbose_name=_("Canal"), max_length=32, blank=True, null=True, default='Website')
    note = models.CharField(verbose_name=_("Observation"), max_length=256, blank=True, null=True, default='Créé automatiquement suite création utilisateur')

    created_by_user = models.CharField(verbose_name=_("Créé par utilisateur"), max_length=64, blank=True, null=True)
    edited_by_user  = models.CharField(verbose_name=_("Modifié par utilisateur"), max_length=64, blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    @property
    def get_postal_address(self):
        pa = self.address1
        if self.address1: pa += f'\n{self.address1}'
        if self.city: pa += f'\n{self.city}'
        if self.state: pa += f'\n{self.state}'
        pa += f'\n{self.country}'
        return pa

    class Meta:
        db_table = 'tenant'
    
    def __str__(self):
        return f'{self.name} - {self.owner}'
    
    def save(self, *args, **kwargs):
        try:
            self.created_by_user = Utilisateur.objects.get(id=self.created_by).username
            self.edited_by_user = Utilisateur.objects.get(id=self.edited_by).username
        except Exception as xc:
            print(f'Error while updating Utilisateur fields: {str(xc)}')
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     print("Deleting object")
    #     super().delete(*args, **kwargs)


class Utilisateur(AbstractBaseUser, PermissionsMixin):

    class CustomUserManager(BaseUserManager):
        def create_user(self, username, email, password=None, **extra_fields):
            if not username:
                raise ValueError("The Username must be set")
            if not email:
                raise ValueError("The Email must be set")

            email = self.normalize_email(email)
            user = self.model(username=username, email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user

        def create_superuser(self, username, email, password=None, **extra_fields):
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            return self.create_user(username, email, password, **extra_fields)


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, blank=True, null=True, related_name="workers")
    verified = models.BooleanField(blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    is_tenant_admin = models.BooleanField(blank=True, null=True)

    created_by = models.UUIDField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(blank=True, null=True)
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        un = self.username
        if self.tenant: un += ' - ' + self.tenant.name
        return un

    class Meta:
        db_table = 'utilisateur'
        verbose_name = "User"
        ordering = ['-is_active', 'tenant', 'created_on', 'last_login', 'is_tenant_admin']


class Trial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    date_fm = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True, editable=False)
    plan = models.ForeignKey('Plan', on_delete=models.RESTRICT, blank=True, null=True, editable=False)
    date_ended = models.DateField(blank=True, null=True, editable=False)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True, editable=False)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'trial'

    def __str__(self):
        return f'TRIAL-{self.plan.name} - {self.tenant.name} - {self.date_fm}_{self.date_to}'


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    # is_trial = models.BooleanField(blank=True, null=True, default=False)
    date_fm = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True)
    plan = models.ForeignKey('Plan', on_delete=models.RESTRICT, blank=True, null=True)
    # payment = models.ForeignKey('SystemPayment', on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True, editable=False)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'subscription'

    def __str__(self):
        return f'{self.plan.name} - {self.tenant.name} - {self.date_fm}_{self.date_to}'


# class SystemPayment(models.Model):
#     class Status(models.TextChoices):
#         DRAFT    = 'D', _('Brouillon')
#         DONE     = 'P', _('Effectué')
#         CANCELED = 'X', _('Annulé')

#     class Modes(models.TextChoices):
#         CASH   = 'C', _('Espèces')
#         WIRE   = 'W', _('Virement')
#         CHECK  = 'K', _('Chèque')
#         ONLINE = 'O', _('Online')
#         OTHER  = 'X', _('Autre')

#     id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active         = models.BooleanField(blank=True, null=True, default=True)
#     status         = models.CharField(max_length=1, choices=Status.choices, default=Status.DRAFT)
#     order_no       = models.CharField(max_length=32, blank=True, null=True)
#     commande       = models.ForeignKey('SystemOrder', on_delete=models.RESTRICT, blank=True, null=True, related_name="payments")
#     verified       = models.BooleanField(blank=True, null=True)
#     reference      = models.CharField(max_length=32, blank=True, null=True)
#     mode           = models.CharField(max_length=1, choices=Modes.choices, default=Modes.WIRE)
#     date_made      = models.DateField(blank=True, null=True)
#     objet          = models.CharField(max_length=128, blank=True, null=True, default= _("Abonnement Application Piecy"))
#     amount         = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     taxes_amount   = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     amount_ttc     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     currency       = models.CharField(max_length=4, blank=True, null=True, default="MAD")
#     made_by        = models.CharField(max_length=64, blank=True, null=True)
#     note           = models.CharField(max_length=64, blank=True, null=True)

#     owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True, editable=False)
#     created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
#     created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
#     edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
#     edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

#     class Meta:
#         db_table = 'system_payment'

#     def __str__(self):
#         prefix = "V" if self.verified else "U"
#         return f'{prefix}#{self.amount}{self.currency}#-{self.made_by}-{self.date_made}-{self.reference}'


# class SystemOrder(models.Model):
#     id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active         = models.BooleanField(blank=True, null=True, default=True)
#     order_no       = models.CharField(max_length=32, blank=True, null=True)
#     order_date     = models.DateTimeField(blank=True, null=True, auto_now_add=True)

#     owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True, editable=False)
#     created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
#     created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
#     edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
#     edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)
    
#     class Meta:
#         db_table = 'system_order'

#     # def __str__(self):
#     #     prefix = "V" if self.verified else "U"
#     #     return f'{prefix}#{self.amount}{self.currency}#-{self.made_by}-{self.date_made}-{self.reference}'


# class SystemOrderLine(models.Model):
#     id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active         = models.BooleanField(blank=True, null=True, default=True)

#     owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True, editable=False)
#     created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
#     created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
#     edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
#     edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)
    
#     class Meta:
#         db_table = 'system_order_line'

#     # def __str__(self):
#     #     prefix = "V" if self.verified else "U"
#     #     return f'{prefix}#{self.amount}{self.currency}#-{self.made_by}-{self.date_made}-{self.reference}'


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    featured = models.BooleanField(blank=True, null=True, default=False)
    name = models.CharField(max_length=16, blank=True, null=True)
    header = models.CharField(max_length=128, blank=True, null=True)
    ordre = models.SmallIntegerField(blank=True, null=True)
    
    year_free_mth = models.SmallIntegerField(blank=True, null=True, default=2)
    first_time_disc = models.SmallIntegerField(blank=True, null=True, default=50)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_taxes = models.SmallIntegerField(blank=True, null=True, default=20)
    currency = models.CharField(max_length=4, blank=True, null=True, default="MAD")

    custom_domain = models.BooleanField(blank=True, null=True)
    mailbox = models.BooleanField(blank=True, null=True)
    ecommerce = models.BooleanField(blank=True, null=True)
    vitrine = models.BooleanField(blank=True, null=True)

    max_users = models.SmallIntegerField(blank=True, null=True)
    max_clients = models.SmallIntegerField(blank=True, null=True)
    max_products = models.SmallIntegerField(blank=True, null=True)
    max_magasins = models.SmallIntegerField(blank=True, null=True)
    max_pdfs = models.SmallIntegerField(blank=True, null=True)
    max_excels = models.SmallIntegerField(blank=True, null=True)

    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True, editable=False)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'plan'
        ordering = ['ordre']

    def __str__(self):
        return f'{self.name}'

    @property
    def monthly_tag_month(self):
        return int(self.monthly_price)

    @property
    def yearly_tag_month(self):
        return int(max((12 -self.year_free_mth), 0) * self.monthly_price/12)

    @property
    def monthly_tag_month_new(self):
        return int(self.monthly_price * self.first_time_disc/100)

    @property
    def yearly_tag_month_new(self):
        return int(max((12 -self.year_free_mth), 0) * self.monthly_price * self.first_time_disc/1200)


    @property
    def monthly_month_tag(self):
        tag = self.monthly_price
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    @property
    def monthly_month_tag_new(self):
        tag = self.monthly_month_tag * Decimal(max(0, min(1, (1 - self.first_time_disc / 100))))
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    @property
    def monthly_year_tag(self):
        tag = 12 * self.monthly_price
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    @property
    def monthly_year_tag_new(self):
        tag = 12 * self.monthly_month_tag_new
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    @property
    def yearly_year_tag(self):
        tag = max((12 - self.year_free_mth), 0) * self.monthly_price
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    @property
    def yearly_year_tag_new(self):
        tag = self.yearly_year_tag * Decimal(max(0, min(1, (1 - self.first_time_disc / 100))))
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    @property
    def yearly_month_tag(self):
        tag = self.yearly_year_tag / 12
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)

    @property
    def yearly_month_tag_new(self):
        tag = self.yearly_year_tag_new / 12
        return Decimal(tag).quantize(Decimal("0"), rounding=ROUND_HALF_UP)


##################################
class SystemOrder(models.Model):
    STATUS_CHOICES = [
        ("pending",   _("Attente paiement")),
        ("partial",   _("Partiellement payé")),
        ("paid",      _("Payé")),
        ("cancelled", _("Annulé")),
    ]

    customer = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_number = models.CharField(max_length=20, unique=True)
    order_date   = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at   = models.DateTimeField(default=timezone.now)
    updated_at   = models.DateTimeField(auto_now=True)
    notes        = models.TextField(blank=True)

    class Meta:
        db_table = 's_order'

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer.name}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def amount_paid(self):
        return self.payments.aggregate(total=models.Sum("amount"))["total"] or Decimal("0.00")

    @property
    def amount_due(self):
        return self.total_amount - self.amount_paid

    def update_status(self):
        paid = self.amount_paid
        if paid == 0:
            self.status = "pending"
        elif paid < self.total_amount:
            self.status = "partial"
        elif paid >= self.total_amount:
            self.status = "paid"
        self.save()


class SystemOrderItem(models.Model):
    order = models.ForeignKey(
        SystemOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product_name = models.CharField(max_length=255)  # could be linked to a Product model if you have one
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_currency = models.CharField(max_length=8, default="MAD")
    quantity = models.PositiveIntegerField(default=1)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # e.g., 15 for 15%

    class Meta:
        db_table = 's_order_item'

    @property
    def total_price(self):
        return self.unit_price * self.quantity
    
    @property
    def tax_amount(self):
        return (self.unit_price * self.quantity) * (self.tax_rate / Decimal("100"))

    @property
    def total_price_with_tax(self):
        return (self.unit_price * self.quantity) + self.tax_amount

    def __str__(self):
        return self.product_name


class SystemPayment(models.Model):
    METHOD_CHOICES = [
        ("cash",          _("Cash")),
        ("bank_transfer", _("Bank Transfer")),
        ("mobile_money",  _("Eléctronique")),
        ("cheque",        _("Chèque")),
        ("other",         _("Autre")),
    ]

    STATUS_CHOICES = [
        ("pending",   _("Pending")),
        ("confirmed", _("Confirmed")),
        ("failed",    _("Failed")),
    ]

    order = models.ForeignKey(
        SystemOrder,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    reference = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    transaction_reference = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 's_payment'

    def __str__(self):
        return f"{self.reference}-#{self.amount}#-{self.order.order_number}"

    def confirm(self):
        """Mark the payment as confirmed and update order status."""
        self.status = "confirmed"
        self.paid_at = timezone.now()
        self.save()
        self.order.update_status()
##################################




class Registre(models.Model):
    OPERATIONS = [('C', 'Create'), ('R', 'Read'), ('U', 'Update'), ('D', 'Delete'),]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    date = models.DateField(blank=True, null=True)
    model = models.CharField(max_length=32, blank=True, null=True)
    instance = models.CharField(max_length=128, blank=True, null=True)
    operation = models.CharField(max_length=1, choices=OPERATIONS, default='C')

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True, editable=False)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'registre'