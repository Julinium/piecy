import uuid #, os
from django.db import models
from django.utils.translation import gettext as _
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
        # if self.pk is None: print("Creating object")
        # else: print("Updating object")
        try:
            self.created_by_user = Utilisateur.objects.get(id=self.created_by).username
            self.edited_by_user = Utilisateur.objects.get(id=self.edited_by).username
        except Exception as xc:
            print(f'Error while updating Utilisateur fields: {str(xc)}')
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     print("Deleting object")
    #     super().delete(*args, **kwargs)


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


class Utilisateur(AbstractBaseUser, PermissionsMixin):
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



class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    is_trial = models.BooleanField(blank=True, null=True, default=False)
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
    
    # def save(self, *args, **kwargs):
    #     if self.is_trial:
    #         try:
    #             tenant = Tenant.objects.filter(tenant=self.tenant).first()
    #             if tenant: 
    #                 tenant.can_try = False
    #                 tenant.save()
    #         except Exception as xc:
    #             print(f'Error while updating Tenant: {str(xc)}')
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.plan.name} - {self.tenant.name} - {self.date_fm}_{self.date_to}'

class SystemPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    verified = models.BooleanField(blank=True, null=True)
    reference = models.CharField(max_length=32, blank=True, null=True)
    mode = models.CharField(max_length=32, blank=True, null=True)
    date_made = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=16, blank=True, null=True, default="MAD")
    maker = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=64, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'system_payment'

    def __str__(self):
        prefix = "VERIF" if self.verified else "UNVERIF"
        return f'{prefix}#{self.amount}{self.currency}#-{self.maker}-{self.date_made}-{self.reference}'


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    header = models.CharField(max_length=128, blank=True, null=True)
    ordre = models.SmallIntegerField(blank=True, null=True)
    
    year_free_mth = models.SmallIntegerField(blank=True, null=True, default=2)
    first_time_disc = models.SmallIntegerField(blank=True, null=True, default=50)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)

    custom_domain = models.BooleanField(blank=True, null=True)
    mailbox = models.BooleanField(blank=True, null=True)
    ecommerce = models.BooleanField(blank=True, null=True)
    vitrine = models.BooleanField(blank=True, null=True)

    max_users = models.SmallIntegerField(blank=True, null=True)
    max_clients = models.SmallIntegerField(blank=True, null=True)
    max_magasins = models.SmallIntegerField(blank=True, null=True)
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
        ordering = ['ordre']
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