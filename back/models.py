import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.utils.translation import gettext as _
from django_currentuser.middleware import get_current_user
from django.utils.timezone import now
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


strapus = {
    "X": "secondary",
    "W": "warning",
    "P": "warning",
    "C": "success",
    "A": "danger",
    }

# If a subscription is unpaid/unconfirmed, it can still be usable for a certain grace time.
# This time is set to a percentage of the subscription duration within a range.
GRACE_DAYS_MIN = 15     # Min grace days.
GRACE_DAYS_MAX = 30     # Max grace days.
GRACE_DAYS_100 = 10     # Grace percentage. Example: 8.22 gives 30 days for a 365 days subscription.


def get_current_user_default():
    """
    Retrieves the current user from the request context.
    """

    user = get_current_user()
    return user if user and user.is_authenticated else None


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(verbose_name=_("Activé"), blank=True, null=True, default=True)
    onboarded = models.BooleanField(verbose_name=_("Onboarded"), blank=True, null=True, default=False)
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
    logo = models.ImageField(verbose_name=_("Logo"), upload_to='tenants/logos/', blank=True, null=True)
    brand = models.ImageField(verbose_name=_("Bannière"), upload_to='tenants/brands/', blank=True, null=True)
    header = models.ImageField(verbose_name=_("En-tête"), upload_to='tenants/headers/', blank=True, null=True)
    footer = models.ImageField(verbose_name=_("Bas de page"), upload_to='tenants/footers/', blank=True, null=True)
    owner = models.CharField(verbose_name=_("Propriétaire"), max_length=64, blank=True, null=True)
    channel = models.CharField(verbose_name=_("Canal"), max_length=32, blank=True, null=True, default='Website')
    note = models.CharField(verbose_name=_("Observation"), max_length=256, blank=True, null=True, default='Créé automatiquement suite création utilisateur')
    created_by = models.ForeignKey('Utilisateur', on_delete=models.RESTRICT, verbose_name=_("Créé par"), related_name="created_tenants", blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('Utilisateur', on_delete=models.RESTRICT, verbose_name=_("Modifié par"), related_name="edited_tenants", blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    @property
    def get_postal_address(self):
        pa = self.address1
        if self.address2: pa += f'\n{self.address2}'
        if self.city: pa += f'\n{self.city}'
        if self.state: pa += f'\n{self.state}'
        pa += f'\n{self.country}'
        return pa

    class Meta:
        db_table = 'tenant'
    
    def __str__(self):
        return f'{self.name} - {self.owner}'


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

    created_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Créé par"), related_name="created_trials", blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Modifié par"), related_name="edited_trials", blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'trial'

    def __str__(self):
        return f'TRIAL-{self.plan.name} - {self.tenant.name} - {self.date_fm}_{self.date_to}'


class Subscription(models.Model):
    
    STATUS_CHOICES = [
        ("X", _("Brouillon")),
        ("W", _("Attente Paiement")),
        ("P", _("Paiement Partiel")),
        ("C", _("Payé")),
        ("A", _("Annulé")),
    ]

    id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active  = models.BooleanField(blank=True, null=True, default=True)
    numero  = models.CharField(max_length=20, unique=True, editable=False)
    date_fm = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    status  = models.CharField(max_length=20, choices=STATUS_CHOICES, default="X")
    tenant  = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True)
    plan    = models.ForeignKey('Plan', on_delete=models.RESTRICT, blank=True, null=True)
    order   = models.ForeignKey('SystemOrder', on_delete=models.RESTRICT, blank=True, null=True, related_name="subscriptions")

    created_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Créé par"), related_name="created_subscriptions", blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Modifié par"), related_name="edited_subscriptions", blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        """ Meta class"""
        db_table = 'subscription'
        ordering = ['-active', 'status', 'date_to']

    def __str__(self):
        return f'{self.plan.name} - {self.tenant.name} - {self.date_fm}_{self.date_to}'

    @property
    def days_span(self):
        """ Days between end and start dates."""

        delta = self.date_to - self.date_fm
        return 1 + delta.days

    @property
    def days_run(self):
        """ Number of elapsed days from start date to d_date."""

        d_date=now().date()
        delta = self.date_to - d_date
        if delta.days <= 0:
            return self.days_span
        delta = d_date - self.date_fm
        if delta.days <= 0:
            return 0        
        return delta.days

    @property
    def progress_percent(self):
        """ Percentage of remaining days (from d_date to end date) divided by total days span."""

        return 100 - int(max(0, min(100, 100 * self.days_run/self.days_span)))

    @property
    def days_to_end(self):
        """ Number of days from d_date to end date, maxed by total days span."""

        d_date=now().date()
        delta = self.date_to - d_date
        return max(0, min(delta.days, self.days_span))

    @property
    def days_grace(self):
        return max(GRACE_DAYS_MIN, min(GRACE_DAYS_MAX, int(self.days_span/Decimal(GRACE_DAYS_100))))

    @property
    def usable(self):
        """ Whether subscription can be used or not."""
        if self.window != 0:
            return False
        if self.status != "C":
            return self.days_run <= self.days_grace
        return True

    @property
    def teint(self):
        """ Return a string indicating the right color to use in bootstrap styling."""

        return strapus[self.status]

    @property
    def window(self):
        """
        Checks if subscription is past, running or upcoming.
        -1 = Past, 0 = Running, 1 = Upcoming and None = Undefined.
        """
        
        d_date=now().date()
        if not self.date_fm or not self.date_to:
            return None
        if self.date_fm > d_date:
            return 1
        if self.date_to < d_date:
            return -1
        return 0
    
    def save(self, *args, **kwargs):
        if not self.numero:
            today = timezone.now().date()
            year_str = today.strftime('%y')
            jan_first = date(today.year, 1, 1)
            days_elapsed = (today - jan_first).days + 1 
            date_str = f'{year_str}{days_elapsed:03d}'
            last_sub = Subscription.objects.filter(created_on__year=today.year).order_by('created_on').last()

            if last_sub:
                last_seq = int(last_sub.numero[-6:])
                new_seq = last_seq + 1
            else:
                new_seq = 1
            self.numero = f'SS{date_str}{new_seq:06d}'
        super().save(*args, **kwargs)

    def update_status(self):
        """ Updates the status field."""
        
        d_date=now().date()
        self.status = "X"
        if self.order:
            if self.order.active:
                self.order.update_status()
                self.status = self.order.status
        self.save()


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

    created_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Créé par"), related_name="created_plans", blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Modifié par"), related_name="edited_plans", blank=True, null=True)
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


class SystemOrder(models.Model):

    STATUS_CHOICES = [
        ("W", _("Attente Paiement")),
        ("P", _("Paiement Partiel")),
        ("C", _("Payée")),
        ("A", _("Annulée")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    customer = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    numero = models.CharField(max_length=20, unique=True, editable=False)
    order_date    = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default="W")
    order_currency = models.CharField(max_length=8, default="MAD")
    notes          = models.TextField(blank=True)
    
    created_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Créé par"), related_name="created_s_orders", blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Modifié par"), related_name="edited_s_orders", blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 's_order'
        ordering = ['-status', '-created_on']

    def __str__(self):
        return self.numero

    @property
    def total_amount(self):
        s = sum(item.total_price for item in self.items.all())
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total_tax_amount(self):
        s = sum(item.tax_amount for item in self.items.all())
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total_amount_with_tax(self):
        s = sum(item.total_price_with_tax for item in self.items.all())
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def amount_paid_confirmed(self):
        s = self.payments.filter(active=True, status="C").aggregate(total=models.Sum("amount"))["total"] or Decimal("0.00")
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def amount_paid_pending(self):
        s = self.payments.filter(active=True, status="W").aggregate(total=models.Sum("amount"))["total"] or Decimal("0.00")
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def amount_due(self):
        s = self.total_amount_with_tax - self.amount_paid_confirmed
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def amount_due_to_pay(self):
        s = self.total_amount_with_tax - self.amount_paid_confirmed - self.amount_paid_pending
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def amount_overpaid(self):
        s = - self.amount_due_to_pay if self.amount_due_to_pay < 0 else 0
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def has_active_payments(self):
        return len(self.payments.filter(active=True)) > 0

    def update_status(self):
        paid = self.amount_paid_confirmed
        if paid == 0:
            if self.amount_paid_pending > 0:
                self.status = "P"
            else:
                self.status = "W"
        elif paid < self.total_amount_with_tax:
            self.status = "P"
        elif paid >= self.total_amount_with_tax:
            self.status = "C"
        self.save()

    def save(self, *args, **kwargs):
        if not self.numero:
            today = timezone.now().date()
            year_str = today.strftime('%y')
            jan_first = date(today.year, 1, 1)
            days_elapsed = (today - jan_first).days + 1 
            date_str = f'{year_str}{days_elapsed:03d}'
            last_order = SystemOrder.objects.filter(created_on__year=today.year).order_by('created_on').last()

            if last_order:
                last_seq = int(last_order.numero[-6:])
                new_seq = last_seq + 1
            else:
                new_seq = 1
            self.numero = f'SO{date_str}{new_seq:06d}'
        super().save(*args, **kwargs)


class SystemOrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    order = models.ForeignKey(
        SystemOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product_name = models.CharField(max_length=255)  # could be linked to a Product model if you have one
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # e.g., 15 for 15%

    class Meta:
        db_table = 's_order_item'

    @property
    def total_price(self):
        s = self.unit_price * self.quantity
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    @property
    def tax_amount(self):
        s = (self.unit_price * self.quantity) * (self.tax_rate / Decimal("100"))
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def total_price_with_tax(self):
        s = (self.unit_price * self.quantity) + self.tax_amount
        return Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return self.product_name


class SystemPayment(models.Model):
    METHOD_CHOICES = [
        ("cash",          _("Cash")),
        ("bank_transfer", _("Transfert bancaire")),
        ("mobile_money",  _("Eléctronique")),
        ("cheque",        _("Chèque")),
        ("other",         _("Autre")),
    ]

    STATUS_CHOICES = [
        ("W", _("Attente Confirmation")),
        ("C", _("Confirmé")),
        ("A", _("Echoué")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    order = models.ForeignKey(
        SystemOrder,
        verbose_name=_("Commande"),
        on_delete=models.CASCADE,
        related_name="payments"
    )

    numero = models.CharField(verbose_name=_("Numéro"), max_length=20, unique=True, editable=False)
    amount = models.DecimalField(verbose_name=_("Montant"), max_digits=10, decimal_places=2)
    method = models.CharField(verbose_name=_("Méthode"), max_length=20, choices=METHOD_CHOICES, default="bank_transfer")
    status = models.CharField(verbose_name=_("Status"), max_length=20, choices=STATUS_CHOICES, default="W")
    reference = models.CharField(verbose_name=_("Référence"), max_length=100, blank=True)
    paid_at = models.DateTimeField(verbose_name=_("Payé le"), null=True, blank=True, default=timezone.now)
    notes = models.TextField(verbose_name=_("Notes"), blank=True)

    created_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Créé par"), related_name="created_s_payments", blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT, default=get_current_user_default, verbose_name=_("Modifié par"), related_name="edited_s_payments", blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 's_payment'
        ordering = ['-status', 'active', '-paid_at', 'order']

    def __str__(self):
        return f"{self.numero}-#{self.amount}#-{self.status}-{self.order.numero}"

    def confirm(self):
        """Mark the payment as confirmed and update order status."""
        self.status = "C"
        self.paid_at = timezone.now()
        self.save()
        self.order.update_status()

    def save(self, *args, **kwargs):
        if not self.numero:
            today = timezone.now().date()   
            year_str = today.strftime('%y')
            jan_first = date(today.year, 1, 1)
            days_elapsed = (today - jan_first).days + 1
            date_str = f'{year_str}{days_elapsed:03d}'
            last_payment = SystemPayment.objects.filter(created_on__year=today.year).order_by('created_on').last()
    
            if last_payment:
                last_seq = int(last_payment.numero[-6:])
                new_seq = last_seq + 1
            else:
                new_seq = 1
            self.numero = f'SP{date_str}{new_seq:06d}'
        super().save(*args, **kwargs)


class Registre(models.Model):
    OPERATIONS = [('C', 'Create'), ('R', 'Read'), ('U', 'Update'), ('D', 'Delete'),]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    date = models.DateField(blank=True, null=True)
    model = models.CharField(max_length=32, blank=True, null=True)
    instance = models.CharField(max_length=128, blank=True, null=True)
    operation = models.CharField(max_length=1, choices=OPERATIONS, default='C')

    class Meta:
        db_table = 'registre'