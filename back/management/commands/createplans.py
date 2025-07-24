from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from datetime import date, timedelta

from back.models import Plan #, Tenant, Utilisateur, Subscription

class Command(BaseCommand):
    help = 'Insert basic Plans data into the database'

    def handle(self, *args, **kwargs):
        # today = date.today()
        plans_data = [
            Plan(
                name = _("Basic"),
                header =  _("L'essentiel pour faire tourner une petite entreprise."),
                ordre = 10,
                monthly_price = 299.00,
                max_users = 2,
                max_clients = 10,
                max_magasins = 2,
                max_products = 50,
                max_pdfs = 50,
                max_excels = 50,
                custom_domain = False,
                mailbox = False,
                ecommerce = False,
                vitrine = True,
            ),

            Plan(
                name = _("Avancé"),
                header =  _("Basic + Fonctionnalités avnacées pour permettre plus d'opérations."),
                ordre = 20,
                monthly_price = 399.00,
                max_users = 10,
                max_clients = 100,
                max_magasins = 5,
                max_products = 500,
                max_pdfs = 500,
                max_excels = 500,
                custom_domain = False,
                mailbox = False,
                ecommerce = False,
                vitrine = True,
            ),

            Plan(
                name = _("Pro"),
                header =  _("Avancé + Tout ce qu'il faut pour bien gérer une grande entreprise."),
                ordre = 30,
                monthly_price = 499.00,
                max_users = 50,
                max_clients = 1000,
                max_magasins = 25,
                max_products = 2000,
                max_pdfs = 2000,
                max_excels = 2000,
                custom_domain = True,
                mailbox = True,
                ecommerce = True,
                vitrine = True,
            ),
        ]

        Plan.objects.bulk_create(plans_data)

        self.stdout.write(self.style.SUCCESS('Data inserted successfully.'))

