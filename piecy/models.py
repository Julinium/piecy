import uuid #, os
from django.db import models
from django.utils.translation import gettext as _
# from accs.models import Utilisateur
from back.models import Tenant
from datetime import date



class Product(models.Model):
    class Conditions(models.TextChoices):
        BRAND_NEW   = 'N', _('Nouveau')
        REFURBISHED = 'R', _('Reconditionné')
        USED        = 'U', _('Utilisé')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    reference = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=128, blank=False, null=False)

    condition = models.CharField(max_length=1, choices=Conditions.choices, default=Conditions.BRAND_NEW)
    um = models.CharField(max_length=16, blank=True, null=True)
    sku = models.CharField(max_length=128, blank=True, null=True)
    group = models.ForeignKey('Group', on_delete=models.RESTRICT, blank=True, null=True)
    fabricant = models.ForeignKey('Fabricant', on_delete=models.RESTRICT, blank=True, null=True)
    origin = models.CharField(max_length=32, blank=True, null=True)
    guarantee = models.SmallIntegerField(blank=True, null=True, default=12)

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

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        p = f'[{self.reference}] {self.name}'
        if self.um: p += f' ({self.um})'
        return p


class Client(models.Model):
    class Civilites(models.TextChoices):
        MR     = 'M', _('Mr.')
        MS     = 'F', _('Mme.')
        ML     = 'L', _('Mlle.')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    civilite = models.CharField(max_length=1, choices=Civilites.choices, default=Civilites.MR)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=False, null=False)

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

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'client'

    def __str__(self):
        callee = ""
        if self.civilite: callee += self.civilite
        if self.first_name: callee += f' {self.first_name}'
        if self.last_name: callee += f' {self.last_name}'
        if self.societe: callee += f' [{self.societe.name}]'
        return callee.strip()


class Clientele(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'clientele'

    def __str__(self):
        return self.name


class Commande(models.Model):
    class Status(models.TextChoices):
        DRAFT     = '1', _('Brouillon')
        QUOTE     = '2', _('Devis')
        ACCEPTED  = '3', _('Acceptée')
        DELIVERED = '4', _('Livrée')
        CANCELLED = '0', _('Annulée')

    class Deliveries(models.TextChoices):
        BUYER      = 'B', _('À la charge du client')
        SELLER     = 'S', _('À la charge du vendeur')
        ACCEPTED   = 'A', _('Agent tiers')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(verbose_name=_("Activée"), blank=True, null=True, default=True)
    status = models.CharField(verbose_name=_("Status"), max_length=1, choices=Status.choices, default=Status.DRAFT)
    client = models.ForeignKey('Client', verbose_name=_("Client"), on_delete=models.RESTRICT, blank=True, null=True)
    order_number = models.CharField(verbose_name=_("Numéro de commande"), max_length=256, blank=True, null=True, default=1)
    order_date = models.DateField(verbose_name=_("Date de commande"), blank=True, null=True, auto_now_add=True)
    total_bt = models.SmallIntegerField(verbose_name=_("Total hors taxes"), blank=True, null=True)
    total_at = models.SmallIntegerField(verbose_name=_("Total TTC"), blank=True, null=True)

    delivery_terms = models.CharField(verbose_name=_("Termes de livraison"), max_length=1, choices=Deliveries.choices, default=Deliveries.BUYER)
    delivery_due_date = models.DateField(verbose_name=_("Date de livraison due"), blank=True, null=True)
    packager = models.CharField(verbose_name=_("Responsable emballage"), max_length=256, blank=True, null=True)
    charger = models.CharField(verbose_name=_("Responsable chargement"), max_length=256, blank=True, null=True)
    delivery_agent = models.CharField(verbose_name=_("Responsable livraison"), max_length=256, blank=True, null=True)
    delivery_mean = models.CharField(verbose_name=_("Moyen livraison"), max_length=256, blank=True, null=True)
    delivery_actual_date = models.DateField(verbose_name=_("Date livraison éffective"), blank=True, null=True)

    payment_done = models.BooleanField(verbose_name=_("Payment effectué"), blank=True, null=True, default=False)
    payment_date_due = models.DateField(verbose_name=_("Date de payment dù"), blank=True, null=True)
    payment_reminder = models.SmallIntegerField(verbose_name=_("Rappel de payment"), blank=True, null=True, default=7)
    global_discount = models.SmallIntegerField(verbose_name=_("Remise globale"), blank=True, null=True)

    file = models.FileField(verbose_name=_("Fichier"), upload_to='orders/', blank=True, null=True)
    note = models.CharField(verbose_name=_("Note"), max_length=256, blank=True, null=True)
    gage = models.CharField(verbose_name=_("Gage ou Garantie"), max_length=64, blank=True, null=True)
    internal_note = models.CharField(verbose_name=_("Note interne"), max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Propriétaire"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'commande'

    def __str__(self):
        cmde = f'[{self.get_total_ttc}] - '
        cmde += f'{self.client.last_name}'
        if self.client.societe : cmde += f' ({self.client.societe.name})'
        return cmde

    
    def save(self, *args, **kwargs):
        self.total_bt = self.get_total_bt
        self.total_at = self.get_total_at
        if not self.pk:
            self.order_number = self.get_order_number
        super().save(*args, **kwargs)

    @property
    def get_order_number(self):
        new_sequence = 1
        latest_order = Commande.objects.latest('order_date')
        d = date().today()
        if self.order_date.year == d.year:
            if latest_order:
                if latest_order.order_number:
                    old_sequence = int(latest_order.order_number[6:])
                    new_sequence = 1 + old_sequence
        year = d.year % 100
        day_of_year = d.timetuple().tm_yday
        return f"C{year:02d}{day_of_year:03d}{new_sequence:5d}"


    @property
    def get_total_bt(self):
        total_bt = 0
        for item in self.sorties:
            total_bt += item.quantity * item.product.prix_vente_public
        return total_bt

    @property
    def get_total_at(self):
        total_ttc = 0
        for item in self.sorties:
            total_ttc += item.quantity * item.product.prix_vente_public * ( 1 + item.product.tva_percent / 100)
        return total_ttc


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    magasin = models.ForeignKey('Magasin', on_delete=models.RESTRICT, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'stock'
    
    def __str__(self):
        d = self.edited_on if self.edited_on else self.created_on
        return f'{self.product.name} - {self.magasin.name} - {d.strftime(("%Y-%m-%d"))}'


class Ensemble(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'ensemble'
    
    def __str__(self):
        return self.name


class Entree(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    reception = models.ForeignKey('Reception', on_delete=models.RESTRICT, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    prix_unit = models.SmallIntegerField(blank=True, null=True, default=0)
    note = models.CharField(max_length=256, blank=True, null=True)
    rayon = models.ForeignKey('Rayon', on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'entree'
    
    def __str__(self):
        dts = self.reception.date_livraison.strftime("%Y-%m-%d")
        return f'{self.quantity} x {self.product.reference} - {self.product.name} - {dts}'


class Fabricant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=16, blank=True, null=True, default='ma')
    website = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=16, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'fabricant'
    
    def __str__(self):
        return self.name


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    upload = models.FileField(upload_to='products/', blank=True, null=True)
    mime = models.CharField(max_length=32, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'file'
    
    def __str__(self):
        return f'{self.name} - {self.upload}'


class Floor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    elevation = models.SmallIntegerField(blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    magasin = models.ForeignKey('Magasin', on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'floor'
    
    def __str__(self):
        return f'{self.magasin.name} - {self.name}'


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

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'fournisseur'
    
    def __str__(self):
        f = self.name
        if self.societe: f += ' - ' + self.societe.name        
        return f


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'group'
    
    def __str__(self):    
        return self.name


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


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

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'magasin'

    def __str__(self):
        return self.name


class ClienteleClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clientele = models.ForeignKey('Clientele', on_delete=models.RESTRICT, blank=True, null=True)
    client = models.ForeignKey('Client', on_delete=models.RESTRICT, blank=True, null=True)
    
    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'clientele_client'

    def __str__(self):
        return f'{self.clientele} _ {self.client}'


class CategoryProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    
    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'category_product'

    def __str__(self):
        return f'{self.category} _ {self.product}'


class EnsembleProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ensemble = models.ForeignKey('Ensemble', on_delete=models.RESTRICT, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    
    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'ensemble_product'

    def __str__(self):
        return f'{self.ensemble} _ {self.product}'


class VehiculeProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicule = models.ForeignKey('Vehicule', on_delete=models.RESTRICT, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    
    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'vehicule_product'

    def __str__(self):
        return f'{self.vehicule} _ {self.product}'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    verified = models.BooleanField(blank=True, null=True)
    commande = models.ForeignKey('Commande', on_delete=models.RESTRICT, blank=True, null=True)
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
        db_table = 'payment'

    def __str__(self):
        soc, cli = None, None
        if self.commande:
            if self.commande.client:
                cli = self.commande.client.name
                if self.commande.client.societe:
                    soc = self.commande.client.societe.name
        p = f'[{self.amount} {self.currency}]'
        if cli: p += ' - ' + cli
        if soc: p += ' - ' + soc
        return p


class Rayon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    number = models.SmallIntegerField(blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    floor = models.ForeignKey('Floor', on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'rayon'

    def __str__(self):
        return f'{self.floor.magasin.name} - {self.floor.name} - {self.name}'


class Reception(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.RESTRICT, blank=True, null=True)
    date_commande = models.DateField(blank=True, null=True)
    date_livraison = models.DateField(blank=True, null=True)
    delivery_data = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True, default=True)
    date_due = models.DateField(blank=True, null=True)
    gage = models.CharField(max_length=64, blank=True, null=True)
    payment_reminder = models.SmallIntegerField(blank=True, null=True, default=7)
    payee = models.BooleanField(blank=True, null=True, default=False)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'reception'


class PaymentFournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    verified = models.BooleanField(blank=True, null=True)
    reception = models.ForeignKey('Reception', on_delete=models.RESTRICT, blank=True, null=True)
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
        db_table = 'payment_fournisseur'

    def __str__(self):
        soc, cli = None, None
        if self.reception:
            if self.reception.fournisseur:
                cli = self.reception.fournisseur.name
                if self.reception.fournisseur.societe:
                    soc = self.reception.fournisseur.societe.name
        p = f'[{self.amount} {self.currency}]'
        if cli: p += ' - ' + cli
        if soc: p += ' - ' + soc
        return p


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
    rc = models.CharField(max_length=64, blank=True, null=True)
    tp = models.CharField(max_length=64, blank=True, null=True)
    rib = models.CharField(max_length=64, blank=True, null=True)

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

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'societe'


class Sortie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, blank=True, null=True)
    commande = models.ForeignKey('Commande', on_delete=models.RESTRICT, related_name='sorties', blank=True, null=True)
    qtte_cmde = models.SmallIntegerField(blank=True, null=True, default=0)
    qtte_recv = models.SmallIntegerField(blank=True, null=True, default=0)
    prix_unit = models.SmallIntegerField(blank=True, null=True, default=0)
    discount = models.SmallIntegerField(blank=True, null=True)
    rayon = models.ForeignKey('Rayon', on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'sortie'


class Vehicule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    marque = models.CharField(max_length=16, blank=True, null=True)
    model_nom = models.CharField(max_length=16, blank=True, null=True)
    model_code = models.CharField(max_length=16, blank=True, null=True)
    year_start = models.DateField(blank=True, null=True)
    year_end = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=16, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'vehicule'


class Constant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True, default=True)
    key = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    note = models.CharField(max_length=256, blank=True, null=True)
    value = models.CharField(max_length=256, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, blank=True, null=True)

    owned_by = models.UUIDField(verbose_name=_("Appartient à"), blank=True, null=True)
    created_by = models.UUIDField(verbose_name=_("Créé par"), blank=True, null=True)
    created_on = models.DateTimeField(verbose_name=_("Créé le"), blank=True, null=True, auto_now_add=True)
    edited_by = models.UUIDField(verbose_name=_("Modifié par"), blank=True, null=True)
    edited_on = models.DateTimeField(verbose_name=_("Modifié le"), blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'constant'
