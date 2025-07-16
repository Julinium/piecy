# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Category(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Checkup(models.Model):
    id = models.UUIDField()
    activee = models.BooleanField()
    date = models.DateField()
    counter = models.CharField(max_length=64, blank=True, null=True)
    reason = models.CharField(max_length=64, blank=True, null=True)
    reference = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)
    id_magasin = models.ForeignKey('Magasin', models.DO_NOTHING, db_column='id_magasin', blank=True, null=True)
    id_count = models.ForeignKey('Count', models.DO_NOTHING, db_column='id_count', blank=True, null=True)
    report = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checkup'


class Client(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
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
    description = models.CharField(max_length=256, blank=True, null=True)
    source = models.CharField(max_length=32, blank=True, null=True)
    id_societe = models.ForeignKey('Societe', models.DO_NOTHING, db_column='id_societe', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'


class Commande(models.Model):
    id = models.UUIDField(primary_key=True)
    activee = models.BooleanField()
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client', blank=True, null=True)
    date_commande = models.DateField(blank=True, null=True)
    date_livraison = models.DateField()
    payee = models.BooleanField()
    report = models.CharField(max_length=256, blank=True, null=True)
    public_note = models.CharField(max_length=256, blank=True, null=True)
    internal_note = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commande'


class Count(models.Model):
    id = models.UUIDField(primary_key=True)
    qtte_cmde = models.SmallIntegerField()
    qtte_recv = models.SmallIntegerField()
    id_rayon = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'count'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Ensemble(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ensemble'


class Entree(models.Model):
    id = models.UUIDField(primary_key=True)
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product', blank=True, null=True)
    id_reception = models.ForeignKey('Reception', models.DO_NOTHING, db_column='id_reception', blank=True, null=True)
    qtte_cmd = models.SmallIntegerField()
    qtte_recv = models.SmallIntegerField()
    id_rayon = models.ForeignKey('Rayon', models.DO_NOTHING, db_column='id_rayon', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entree'


class Fabricant(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=16, blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=16, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fabricant'


class File(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    path = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product', blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file'


class Floor(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    elevation = models.SmallIntegerField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    id_magasin = models.ForeignKey('Magasin', models.DO_NOTHING, db_column='id_magasin', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'floor'


class Fournisseur(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
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
    description = models.CharField(max_length=256, blank=True, null=True)
    source = models.CharField(max_length=32, blank=True, null=True)
    id_societe = models.ForeignKey('Societe', models.DO_NOTHING, db_column='id_societe', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fournisseur'


class Group(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group'


class Magasin(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=16, blank=True, null=True)
    state = models.CharField(max_length=16, blank=True, null=True)
    country = models.CharField(max_length=16, blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)
    manager = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'magasin'


class ManyCategoryHasManyProduct(models.Model):
    pk = models.CompositePrimaryKey('id_category', 'id_product')
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'many_category_has_many_product'


class ManyEnsembleHasManyProduct(models.Model):
    pk = models.CompositePrimaryKey('id_ensemble', 'id_product')
    id_ensemble = models.ForeignKey(Ensemble, models.DO_NOTHING, db_column='id_ensemble')
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'many_ensemble_has_many_product'


class ManyVehiculeModelHasManyProduct(models.Model):
    pk = models.CompositePrimaryKey('id_vehicule_model', 'id_product')
    id_vehicule_model = models.ForeignKey('VehiculeModel', models.DO_NOTHING, db_column='id_vehicule_model')
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'many_vehicule_model_has_many_product'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    verified = models.BooleanField(blank=True, null=True)
    reference = models.CharField(max_length=32, blank=True, null=True)
    mode = models.CharField(max_length=32, blank=True, null=True)
    date_made = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=16, blank=True, null=True)
    maker = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'


class Plan(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    label = models.CharField(max_length=64, blank=True, null=True)
    year_free_mth = models.SmallIntegerField(blank=True, null=True)
    first_time_disc = models.SmallIntegerField(blank=True, null=True)
    monthy_price = models.DecimalField(max_digits=12, decimal_places=2)
    custom_domain = models.BooleanField(blank=True, null=True)
    mailbox = models.BooleanField(blank=True, null=True)
    ecommerce = models.BooleanField(blank=True, null=True)
    vitrine = models.BooleanField(blank=True, null=True)
    max_users = models.SmallIntegerField(blank=True, null=True, db_comment='Max number of users, including admins. 0 is unlimited')
    max_clients = models.SmallIntegerField(blank=True, null=True, db_comment='Max number of clients. 0 is unlimited')
    max_products = models.SmallIntegerField(blank=True, null=True, db_comment='Max number of products. 0 is unlimited')
    max_pdfs = models.SmallIntegerField(blank=True, null=True)
    max_excels = models.SmallIntegerField(blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan'


class Product(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=128)
    label = models.CharField(max_length=64, blank=True, null=True)
    um = models.CharField(max_length=16, blank=True, null=True)
    reference = models.CharField(max_length=64, blank=True, null=True)
    sku = models.CharField(max_length=128, blank=True, null=True)
    id_fabricant = models.ForeignKey(Fabricant, models.DO_NOTHING, db_column='id_fabricant', blank=True, null=True)
    id_group = models.ForeignKey(Group, models.DO_NOTHING, db_column='id_group', blank=True, null=True)
    origin = models.CharField(max_length=32, blank=True, null=True)
    barcode = models.CharField(max_length=256, blank=True, null=True)
    tva_percent = models.SmallIntegerField(blank=True, null=True)
    prix_vente_public = models.SmallIntegerField(blank=True, null=True)
    prix_vente_online = models.SmallIntegerField(blank=True, null=True)
    list_online = models.BooleanField(blank=True, null=True)
    max_discount = models.SmallIntegerField(blank=True, null=True)
    expires = models.BooleanField(blank=True, null=True)
    dimension_l_cm = models.SmallIntegerField(blank=True, null=True)
    dimension_w_cm = models.SmallIntegerField(blank=True, null=True)
    dimension_h_cm = models.SmallIntegerField(blank=True, null=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Rayon(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    number = models.SmallIntegerField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    id_floor = models.ForeignKey(Floor, models.DO_NOTHING, db_column='id_floor', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rayon'


class Reception(models.Model):
    id = models.UUIDField(primary_key=True)
    date_commande = models.DateField(blank=True, null=True)
    date_livraison = models.DateField()
    activee = models.BooleanField()
    payee = models.BooleanField()
    id_fournisseur = models.ForeignKey(Fournisseur, models.DO_NOTHING, db_column='id_fournisseur', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reception'


class Registre(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    model = models.CharField(max_length=32, blank=True, null=True)
    operation = models.CharField(max_length=1, blank=True, null=True)
    record = models.UUIDField(blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registre'


class Societe(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    raison_social = models.CharField(max_length=128, blank=True, null=True)
    forme = models.CharField(max_length=16, blank=True, null=True)
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
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'societe'


class Sortie(models.Model):
    id = models.UUIDField(primary_key=True)
    id_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='id_product', blank=True, null=True)
    id_commande = models.ForeignKey(Commande, models.DO_NOTHING, db_column='id_commande', blank=True, null=True)
    qtte_cmde = models.SmallIntegerField()
    qtte_recv = models.SmallIntegerField()
    id_rayon = models.ForeignKey(Rayon, models.DO_NOTHING, db_column='id_rayon', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sortie'


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=16, blank=True, null=True)
    date_fm = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    id_tenant = models.ForeignKey('Tenant', models.DO_NOTHING, db_column='id_tenant', blank=True, null=True)
    id_plan = models.ForeignKey(Plan, models.DO_NOTHING, db_column='id_plan', blank=True, null=True)
    id_payment = models.ForeignKey(Payment, models.DO_NOTHING, db_column='id_payment', blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscription'


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    tel = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=16, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    whatsapp = models.CharField(max_length=16, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    owner = models.CharField(max_length=64, blank=True, null=True)
    channel = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tenant'


class User(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    id_tenant = models.ForeignKey(Tenant, models.DO_NOTHING, db_column='id_tenant', blank=True, null=True)
    verified = models.BooleanField(blank=True, null=True)
    username = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class VehiculeModel(models.Model):
    id = models.UUIDField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    marque = models.CharField(max_length=16, blank=True, null=True)
    model_nom = models.CharField(max_length=16, blank=True, null=True)
    model_code = models.CharField(max_length=16, blank=True, null=True)
    year_start = models.DateField(blank=True, null=True)
    year_end = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=16, blank=True, null=True)
    created_by = models.UUIDField()
    created_on = models.DateField(blank=True, null=True)
    edited_by = models.UUIDField()
    edited_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicule_model'




# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)