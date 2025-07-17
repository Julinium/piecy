# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

import uuid #, os
from django.db import models
from django.utils.translation import gettext as _
from datetime import date, datetime

# from django.contrib.auth.models import User
# from base.storage import OverwriteStorage



class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_categories')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_categories')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_category'

    def __str__(self):
        return self.name


class Checkup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    date = models.DateField(blank=False, null=False, auto_now_add=True)
    counter = models.CharField(max_length=64, blank=True, null=True)
    reason = models.CharField(max_length=64, blank=True, null=True)
    reference = models.CharField(max_length=128, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    magasin = models.ForeignKey('Magasin', on_delete=models.RESTRICT, blank=True, null=True)
    document = models.CharField(max_length=256, blank=True, null=True)
    
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_checkups')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_checkups')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_checkup'
        
    def __str__(self):
        return f'{self.magasin.name} - {self.date.strftime("%Y-%m-%d")}'


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    civilite = models.CharField(max_length=8, blank=True, null=True, default='Mr.')
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=False, null=False)
    # name = models.CharField(max_length=128)

    address_l1 = models.CharField(max_length=64, blank=True, null=True)
    address_l2 = models.CharField(max_length=64, blank=True, null=True)
    address_city = models.CharField(max_length=32, blank=True, null=True)
    address_state = models.CharField(max_length=32, blank=True, null=True)
    address_country = models.CharField(max_length=32, blank=True, null=True)
    address_zip = models.CharField(max_length=8, blank=True, null=True)
    
    tel = models.CharField(max_length=16, blank=True, null=True)
    mobile = models.CharField(max_length=16, blank=True, null=True)
    whatsapp = models.CharField(max_length=16, blank=True, null=True)
    fax = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    website = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    source = models.CharField(max_length=32, blank=True, null=True)
    societe = models.ForeignKey('Societe', on_delete=models.RESTRICT, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_clients')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_clients')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_client'

    def __str__(self):
        callee = ""
        if self.civilite: callee += self.civilite
        if self.first_name: callee += f' {self.first_name}'
        if self.last_name: callee += f' {self.last_name}'
        if self.societe: callee += f' [{self.societe.name}]'
        return callee.strip()


class Commande(models.Model):
    # class Status(models.TextChoices):
    #     DRAFT     = 'D', _('Draft')
    #     QUOTE     = 'Q', _('Quote')
    #     UNPAID    = 'U', _('Unpaid')
    #     PAID      = 'P', _('Paid')
    #     CANCELLED = 'X', _('Cancelled')
    #     # TODO: Partial payments ?

    # status = models.CharField(max_length=1, choices=Formes.choices, default=Formes.SARL)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    client = models.ForeignKey("Client", on_delete=models.RESTRICT, blank=True, null=True)
    date_commande = models.DateField(blank=True, null=True)
    date_livraison = models.DateField(blank=True, null=True, auto_now_add=True)
    payee = models.BooleanField(blank=True, null=True, default=False)
    document = models.CharField(max_length=256, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    internal_note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_commandes')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_commandes')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_commande'

    @property
    def get_total_ht(self):
        total_bt = 0
        for item in self.sorties:
            total_bt += item.qtte_recv * item.product.prix_vente_public
        return total_bt

    @property
    def get_total_ttc(self):
        total_ttc = 0
        for item in self.sorties:
            total_ttc += item.qtte_recv * item.product.prix_vente_public * ( 1 + item.product.tva_percent / 100)
        return total_ttc

    
    def __str__(self):
        cmde = f'[{self.get_total_ttc}] - '
        cmde += f'{self.client.last_name}'
        if self.client.societe : cmde += f' ({self.client.societe.name})'



class Count(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    checkup = models.ForeignKey('Checkup', on_delete=models.RESTRICT, blank=True, null=True)
    qtte_reelle = models.SmallIntegerField(blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_counts')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_counts')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_count'
    
    def __str__(self):
        return f'{self.product.name} - {self.checkup.date.strftime(("%Y-%m-%d"))}' 


class Ensemble(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_ensembles')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_ensembles')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_ensemble'
    
    def __str__(self):
        return self.name


class Entree(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    reception = models.ForeignKey('Reception', on_delete=models.RESTRICT, blank=True, null=True)
    qtte_cmd = models.SmallIntegerField(blank=True, null=True, default=0)
    qtte_recv = models.SmallIntegerField(blank=True, null=True, default=0)
    note = models.CharField(max_length=256, blank=True, null=True)
    rayon = models.ForeignKey('Rayon', on_delete=models.RESTRICT, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_entries')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_entries')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_entree'
    
    def __str__(self):
        return f'{self.qtte_recv} x {self.product.reference} - {self.reception.date_livraison.strftime("%Y-%m-%d")}'


class Fabricant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=16, blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=16, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_fabricants')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_fabricants')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_fabricant'


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    path = models.CharField(max_length=256, blank=True, null=True)
    mime = models.CharField(max_length=32, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_files')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_files')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_file'


class Floor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    elevation = models.SmallIntegerField(blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    magasin = models.ForeignKey('Magasin', on_delete=models.RESTRICT, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_floors')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_floors')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_floor'


class Fournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=128)

    address_l1 = models.CharField(max_length=64, blank=True, null=True)
    address_l2 = models.CharField(max_length=64, blank=True, null=True)
    address_city = models.CharField(max_length=32, blank=True, null=True)
    address_state = models.CharField(max_length=32, blank=True, null=True)
    address_country = models.CharField(max_length=32, blank=True, null=True)
    address_zip = models.CharField(max_length=8, blank=True, null=True)

    tel = models.CharField(max_length=16, blank=True, null=True)
    mobile = models.CharField(max_length=16, blank=True, null=True)
    whatsapp = models.CharField(max_length=16, blank=True, null=True)
    fax = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    website = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    source = models.CharField(max_length=32, blank=True, null=True)
    societe = models.ForeignKey('Societe', on_delete=models.RESTRICT, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_fournisseurs')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_fournisseurs')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_fournisseur'


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_group')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_group')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_group'


class Magasin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=16, blank=True, null=True)
    state = models.CharField(max_length=16, blank=True, null=True)
    country = models.CharField(max_length=16, blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)
    manager = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_magasin')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_magasin')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_magasin'


class CategoryProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('Category', on_delete=models.RESTRICT)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT)
    
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_categ_prod')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_categ_prod')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_category_product'


class EnsembleProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.RESTRICT)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT)
    
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_ensemble_prod')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_ensemble_prod')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_ensemble_product'


class VehiculeProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicule_model = models.ForeignKey('VehiculeModel', on_delete=models.RESTRICT)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT)
    
    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_vehic_prod')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_vehic_prod')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_vehicule_product'


# class SystemPayment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active = models.BooleanField(blank=True, null=True, default=True)
#     verified = models.BooleanField(blank=True, null=True)
#     reference = models.CharField(max_length=32, blank=True, null=True)
#     mode = models.CharField(max_length=32, blank=True, null=True)
#     date_made = models.DateField(blank=True, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     currency = models.CharField(max_length=16, blank=True, null=True)
#     maker = models.CharField(max_length=64, blank=True, null=True)
#     note = models.CharField(max_length=64, blank=True, null=True)

#     created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_system_payment')
#     created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#     edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_system_payment')
#     edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

#     class Meta:
#         managed = False
#         db_table = 'base_tab_system_payment'


# class Plan(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active = models.BooleanField(blank=True, null=True, default=True)
#     name = models.CharField(max_length=16, blank=True, null=True)
#     header = models.CharField(max_length=128, blank=True, null=True)
#     ordre = models.SmallIntegerField(blank=True, null=True)
#     cta = models.CharField(max_length=128, blank=True, null=True, default=_('Free quote'))
    
#     year_free_mth = models.SmallIntegerField(blank=True, null=True, default=2)
#     first_time_disc = models.SmallIntegerField(blank=True, null=True, default=50)
#     monthly_price = models.DecimalField(max_digits=10, decimal_places=2)

#     custom_domain = models.BooleanField(blank=True, null=True)
#     mailbox = models.BooleanField(blank=True, null=True)
#     ecommerce = models.BooleanField(blank=True, null=True)
#     vitrine = models.BooleanField(blank=True, null=True)

#     max_users = models.SmallIntegerField(blank=True, null=True)
#     max_clients = models.SmallIntegerField(blank=True, null=True)
#     max_products = models.SmallIntegerField(blank=True, null=True)
#     max_pdfs = models.SmallIntegerField(blank=True, null=True)
#     max_excels = models.SmallIntegerField(blank=True, null=True)

#     note = models.CharField(max_length=256, blank=True, null=True)

#     created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_plans')
#     created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#     edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_plans')
#     edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

#     class Meta:
#         managed = False
#         db_table = 'base_tab_plan'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    reference = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=128, blank=False, null=False)

    um = models.CharField(max_length=16, blank=True, null=True)
    sku = models.CharField(max_length=128, blank=True, null=True)
    group = models.ForeignKey('Group', on_delete=models.RESTRICT, blank=True, null=True)
    fabricant = models.ForeignKey('Fabricant', on_delete=models.RESTRICT, blank=True, null=True)
    origin = models.CharField(max_length=32, blank=True, null=True)

    barcode = models.CharField(max_length=256, blank=True, null=True)
    tva_percent = models.SmallIntegerField(blank=True, null=True)
    prix_vente_public = models.SmallIntegerField(blank=True, null=True)
    prix_vente_online = models.SmallIntegerField(blank=True, null=True)
    list_online = models.BooleanField(blank=True, null=True)
    max_discount = models.SmallIntegerField(blank=True, null=True)

    dimension_l_cm = models.SmallIntegerField(blank=True, null=True, default=50)
    dimension_w_cm = models.SmallIntegerField(blank=True, null=True, default=20)
    dimension_h_cm = models.SmallIntegerField(blank=True, null=True, default=30)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    expires = models.BooleanField(blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_products')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_products')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_product'

    def __str__(self):
        return f'[{self.reference}] {self.name}'


class Rayon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    number = models.SmallIntegerField(blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    floor = models.ForeignKey('Floor', on_delete=models.RESTRICT, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_rayon')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_rayon')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_rayon'

    def __str__(self):
        return f'{self.floor.magasin.name} - {self.floor.name} - {self.name}'


class Reception(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_commande = models.DateField(blank=True, null=True)
    date_livraison = models.DateField()
    active = models.BooleanField(blank=True, null=True, default=True)
    payee = models.BooleanField(blank=True, null=True, default=False)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.RESTRICT, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_reception')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_reception')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_reception'


# class Registre(models.Model):
#     OPERATIONS = [('C', 'Create'), ('R', 'Read'), ('U', 'Update'), ('D', 'Delete'),]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active = models.BooleanField(blank=True, null=True, default=True)
#     date = models.DateField(blank=True, null=True)
#     model = models.CharField(max_length=32, blank=True, null=True)
#     instance = models.CharField(max_length=128, blank=True, null=True)
#     operation = models.CharField(max_length=1, choices=OPERATIONS, default='C')

#     created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_registre')
#     created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#     edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_registre')
#     edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

#     class Meta:
#         managed = False
#         db_table = 'base_tab_registre'


class Societe(models.Model):
    class Formes(models.TextChoices):
        SARL  = 'L', 'SARL'
        SA    = 'A', 'SA'
        SNC   = 'N', 'SNC'
        SCS   = 'S', 'SCS'
        SCA   = 'B', 'SCA'
        EI    = 'I', 'EI'
        AE    = 'P', 'AUTO-ENTREP.'
        COOP  = 'C', 'COOPERATIVE'
        ETAT  = 'E', 'ETAT'
        AUTRE = 'X', '-AUTRE-'
        # Usage in code:
        # societe.forme = societe.Formes.SARL
        # print(societe.get_forme_display())  # "SARL" 

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    raison_social = models.CharField(max_length=128, blank=True, null=True)
    forme = models.CharField(max_length=1, choices=Formes.choices, default=Formes.SARL)
    ice = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    manager = models.CharField(max_length=64, blank=True, null=True)
    date_est = models.DateField(blank=True, null=True)
    sector = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    fax = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    website = models.CharField(max_length=64, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_soocietes')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_societes')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_societe'


class Sortie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    commande = models.ForeignKey('Commande', on_delete=models.RESTRICT, related_name='sorties', blank=True, null=True)
    qtte_cmde = models.SmallIntegerField(blank=True, null=True, default=0)
    qtte_recv = models.SmallIntegerField(blank=True, null=True, default=0)
    rayon = models.ForeignKey('Rayon', on_delete=models.RESTRICT, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_sorties')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_sorties')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_sortie'


# class Subscription(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active = models.BooleanField(blank=True, null=True, default=True)
#     name = models.CharField(max_length=16, blank=True, null=True)
#     date_fm = models.DateField(blank=True, null=True)
#     date_to = models.DateField(blank=True, null=True)
#     tenant = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True)
#     plan = models.ForeignKey('Plan', on_delete=models.RESTRICT, blank=True, null=True)
#     payment = models.ForeignKey('SystemPayment', on_delete=models.RESTRICT, blank=True, null=True)

#     created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_subscriptions')
#     created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#     edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_subscriptions')
#     edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

#     class Meta:
#         managed = False
#         db_table = 'base_tab_subscription'


# class Tenant(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active = models.BooleanField(blank=True, null=True, default=True)
#     name = models.CharField(max_length=128, blank=True, null=True)
#     tel = models.CharField(max_length=16, blank=True, null=True)
#     email = models.CharField(max_length=16, blank=True, null=True)
#     phone = models.CharField(max_length=16, blank=True, null=True)
#     whatsapp = models.CharField(max_length=16, blank=True, null=True)
#     domain = models.CharField(max_length=32, blank=True, null=True)
#     slug = models.CharField(max_length=32, blank=True, null=True)
#     owner = models.CharField(max_length=64, blank=True, null=True)
#     channel = models.CharField(max_length=32, blank=True, null=True)
#     note = models.CharField(max_length=256, blank=True, null=True)

#     created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_tenants')
#     created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#     edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_tenants')
#     edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

#     class Meta:
#         managed = False
#         db_table = 'base_tab_tenant'


# class User(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     active = models.BooleanField(blank=True, null=True, default=True)
#     tenant = models.ForeignKey('Tenant', on_delete=models.RESTRICT, blank=True, null=True)
#     verified = models.BooleanField(blank=True, null=True)
#     username = models.CharField(max_length=16, blank=True, null=True)
#     email = models.CharField(max_length=64, blank=True, null=True)
#     phone = models.CharField(max_length=64, blank=True, null=True)
#     first_name = models.CharField(max_length=64, blank=True, null=True)
#     last_name = models.CharField(max_length=64, blank=True, null=True)
#     is_superuser = models.BooleanField(blank=True, null=True)
#     is_admin = models.BooleanField(blank=True, null=True)

#     created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_users')
#     created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#     edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_users')
#     edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

#     class Meta:
#         managed = False
#         db_table = 'base_tab_user'


class VehiculeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    marque = models.CharField(max_length=16, blank=True, null=True)
    model_nom = models.CharField(max_length=16, blank=True, null=True)
    model_code = models.CharField(max_length=16, blank=True, null=True)
    year_start = models.DateField(blank=True, null=True)
    year_end = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=16, blank=True, null=True)

    created_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='created_vehicles')
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edited_by = models.ForeignKey('User', on_delete=models.RESTRICT, blank=False, null=False, related_name='edited_vehicles')
    edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'base_tab_vehicule_model'
