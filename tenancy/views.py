import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
# from datetime import date, datetime, timedelta, timezone
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Case, When, Value, BooleanField

from decimal import Decimal, ROUND_HALF_UP

from django.http import HttpResponse

from back.models import SystemPayment, Plan, Subscription, Trial, Utilisateur, Tenant, SystemOrder

from .forms import CustomUserCreationForm


SUB_DAYS_WARNING = 90
SUB_DAYS_DANGER = 30
SUBS_HISTORY_COUNT = 10

TRIAL_DAYS = 30

today = now().date()


def can_admin(request) -> tuple[int, str]:
    """
    Checks wether or not logged in user can perform administrative tasks.
    """
    user = request.user
    if not user:
        return 404, _("User not found")
    if not user.is_active:
        return 403, _("User Inactive")
    if not user.is_authenticated:
        return 403, _("User not authenticated")
    if not user.is_tenant_admin:
        return 403, _("User not an Admin")
    tenant = user.tenant
    if not tenant:
        return 404, _("Tenant not found")
    if not tenant.active:
        return 403, _("Tenant Inactive")

    return 200, _("OK")


def is_deletable(request, user=None):
    """
    Checks if a give user instance can be safely deleted
    """
    # deletable = False
    reason = _("Intégrité des données")
    if user:
        if request.user:
            if request.user != user:
                if not user.last_login:
                    # TODO: Check user related objects/instances in database.
                    return True, ""
                else:
                    reason = _("Déjà connecté")
    return False, reason


@login_required(login_url="account_login")
def summary(request):
    code, message = can_admin(request)
    if code == 200:
        tenant = request.user.tenant
        tenant_admins = tenant.workers.filter(is_tenant_admin = True)
        tenant_users = tenant.workers.exclude(is_tenant_admin = True)
        payments_count = 0

        context = {
            "tenant" : tenant,
            "admins" : tenant_admins,
            "users"  : tenant_users,
            "payments_count"  : payments_count,
        }

        context["users_count"] = len(tenant_users) + len(tenant_admins)

        subscriptions         = Subscription.objects.filter(tenant=tenant, active=True).order_by('-date_to')
        running_subscriptions = subscriptions.filter(date_fm__lte=today, date_to__gte=today)
        current_subscription  = running_subscriptions.last()

        trials = Trial.objects.filter(active=True, tenant=tenant)
        active_trials = trials.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_trial = active_trials.last()

        max_users = 0
        if current_subscription:
            max_users = current_subscription.plan.max_users

        else:
            if current_trial:
                max_users = current_trial.plan.max_users
        context["max_users"] = max_users

        payments_count = 0
        if subscriptions:
            # payments_count = subscriptions.filter(payment__isnull=False).count()
            # context ["payments_count"] = payments_count
            context ["box"] = "S1R0"
            context ["subscriptions"] = subscriptions[:SUBS_HISTORY_COUNT]
            subscription_remaining_days = 0
            latest_subscription = subscriptions.latest('date_to')
            periodicity = _("Paiement Annuel")
            duracity = latest_subscription.date_to - latest_subscription.date_fm
            if duracity.days < 32:
                periodicity = _("Paiement Mensuel")
                
            context ["periodicity"] = periodicity
            context ["latest_subscription"] = latest_subscription

            if current_subscription:
                context ["box"] = "S1R1"
                context ["current_subscription"] = current_subscription
                delta = current_subscription.date_to - today
                subscription_remaining_days = delta.days

                subscription_duration = 0 
                if current_subscription.date_fm and current_subscription.date_to:
                    subscription_duration = current_subscription.date_to - current_subscription.date_fm

                subscription_percentage = 0
                if subscription_duration.days != 0: 
                    subscription_percentage = min(100, int(100 * subscription_remaining_days/subscription_duration.days))
                context["subscription_percentage"] = subscription_percentage

            context ["subscription_remaining_days"] = subscription_remaining_days

            styling_tint = 'secondary'
            if subscription_remaining_days >= SUB_DAYS_WARNING:
                styling_tint = "success"
            elif SUB_DAYS_DANGER <= subscription_remaining_days < 90: 
                styling_tint = "warning"
            elif subscription_remaining_days < SUB_DAYS_DANGER: 
                styling_tint = "danger"
            context ["styling_tint"] = styling_tint

            return render(request, 'tenancy/summary.html', context)

        trials = Trial.objects.filter(tenant=tenant, active=True)
        if not trials:
            context ["box"] = "S0T0"
            return render(request, 'tenancy/summary.html', context)

        context["trials"] = trials
        running_trials = trials.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_trial  = running_trials.last()

        if current_trial:
            context ["box"] = "S0T1R1"
            context["current_trial"] = current_trial
            delta = current_trial.date_to - today
            trial_remaining_days = delta.days
            context["trial_remaining_days"] = trial_remaining_days
            trial_percentage = 0
            if TRIAL_DAYS != 0: 
                trial_percentage = min(100, int(100 * trial_remaining_days/TRIAL_DAYS))
            context["trial_percentage"] = trial_percentage

            return render(request, 'tenancy/summary.html', context)

        latest_trial = trials.latest('date_to')
        context ["latest_trial"] = latest_trial
        context ["box"] = "S0T1R0"
        return render(request, 'tenancy/summary.html', context)

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def users(request):
    code, message = can_admin(request)
    if code == 200:
        context = {}
        tenant = request.user.tenant

        context["tenant"] = tenant
        tenant_users = Utilisateur.objects.filter(tenant=tenant).annotate(
            is_current_user=Case(When(
                pk=request.user.pk, 
                then=Value(True)
            ), default=Value(False), output_field=BooleanField(), )).order_by(
                "-is_current_user", "-is_active", "-is_tenant_admin", "-last_login", "username"
                )

        max_users = 0
        subscriptions = Subscription.objects.filter(tenant=tenant, active=True).order_by('-date_to')
        running_subscriptions = subscriptions.filter(date_fm__lte=today, date_to__gte=today)
        current_subscription  = running_subscriptions.last()

        trials = Trial.objects.filter(active=True, tenant=tenant)
        active_trials = trials.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_trial = active_trials.last()

        if current_subscription:
            max_users = current_subscription.plan.max_users

        else:
            if current_trial:
                max_users = current_trial.plan.max_users

        context["current_subscription"] = current_subscription
        context["max_users"] = max_users
        context["users_count"] = len(tenant_users)
        context["users"] = tenant_users
        return render(request, 'tenancy/users.html', context)

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def add_user(request):
    code, message = can_admin(request)
    if code == 200:
        context = {}
        tenant_out = request.user.tenant
        context["tenant"] = tenant_out
        subscriptions = Subscription.objects.filter(active=True, tenant=tenant_out)
        active_subscriptions = subscriptions.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_subscription = active_subscriptions.last()
        all_users = Utilisateur.objects.filter(tenant=tenant_out)

        trials = Trial.objects.filter(active=True, tenant=tenant_out)
        active_trials = trials.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_trial = active_trials.last()

        max_users = 0

        if current_subscription:
            max_users = current_subscription.plan.max_users

        else:
            if current_trial:
                max_users = current_trial.plan.max_users

        if max_users > 0:

            if max_users <= len(all_users):
                messages.error(request, _("Nombre maximum d'utilisateur atteint pour votre Plan."))
                return redirect('tenancy_users')

            if request.method == "POST":
                form = CustomUserCreationForm(request.POST)
                if form.is_valid():
                    new_user = form.save(commit=False)
                    new_user.tenant = request.user.tenant
                    new_user.created_by = request.user.id
                    new_user.save()
                    messages.success(request, _("Utilisateur ajouté") + " : " + new_user.username)
                else:
                    messages.error(request, _("Données invalides. Utilisateur non ajouté."))
                return redirect("tenancy_users")

            form = CustomUserCreationForm()
            context["form"] = form

            return render(request, "tenancy/add_user.html", context)

        messages.error(request, _("Vous ne pouvez pas ajouter un Utilisateur."))
        return redirect('tenancy_summary')

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def enable_user(request, user_id=None):
    code, message = can_admin(request)
    if code == 200:
        if user_id:
            user_uuid = uuid.UUID(user_id, version=4)
            try:
                passed_user = Utilisateur.objects.get(id=user_uuid)
                if passed_user:
                    passed_user.is_active = True
                    passed_user.save()
            except Exception as xc:
                print(f"Error while enabling user with id {user_id}: {str(xc)}")
            messages.success(request, _("Utilisateur activé") + " : " + passed_user.username)

            return redirect('tenancy_users')

        return HttpResponse(_("Utilisateur non trouvé."), status=code)
    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def disable_user(request, user_id=None):
    code, message = can_admin(request)
    if code == 200:
        if user_id:
            user_uuid = uuid.UUID(user_id, version=4)
            try:
                passed_user = Utilisateur.objects.get(id=user_uuid)
                if passed_user:
                    if passed_user == request.user :
                        messages.error(request, _("Vous ne pouvez pas désactiver votre propre compte."))
                        return redirect('tenancy_users')
                    passed_user.is_active = False
                    passed_user.save()
            except Exception as xc:
                print(f"Error while disabling user with id {user_id}: {str(xc)}")
            messages.success(request, _("Utilisateur désactivé") + " : " + passed_user.username)

            return redirect('tenancy_users')

        return HttpResponse(_("Utilisateur non trouvé."), status=code)
    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def delete_user(request, user_id=None):
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=403)
    code, message = can_admin(request)
    if code == 200:
        if user_id:
            user_uuid = uuid.UUID(user_id, version=4)
            try:
                passed_user = Utilisateur.objects.get(id=user_uuid)
                passed_username = passed_user.username
                if passed_user:
                    if passed_user == request.user :
                        messages.error(request, _("Vous ne pouvez pas supprimer votre propre compte."))
                        return redirect('tenancy_users')
                    deletable, reason = is_deletable(request, passed_user)
                    if deletable :
                        passed_user.delete()
                    else:
                        messages.error(request, passed_username + " : " + _("Vous ne pouvez pas supprimer cet Utilisateur") + ". " + _("Raison") + ": " + reason)
                        return redirect('tenancy_users')
            except Exception as xc:
                print(f"Error while disabling user with id {user_id}: {str(xc)}")
            messages.success(request, _("Utilisateur supprimeé") + " : " + passed_username)

            return redirect('tenancy_users')

        return HttpResponse(_("Utilisateur non trouvé."), status=code)
    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def disadminize_user(request, user_id=None):
    code, message = can_admin(request)
    if code == 200:
        if user_id:
            user_uuid = uuid.UUID(user_id, version=4)
            try:
                passed_user = Utilisateur.objects.get(id=user_uuid)
                if passed_user:
                    if passed_user == request.user :
                        messages.error(request, _("Vous ne pouvez pas rendre votre propre compte Non-Admin."))
                        return redirect('tenancy_users')
                    passed_user.is_tenant_admin = False
                    passed_user.save()
            except Exception as xc:
                print(f"Error while enabling user with id {user_id}: {str(xc)}")
            messages.success(request, _("Utilisateur rendu Non-Admin") + " : " + passed_user.username)

            return redirect('tenancy_users')

        return HttpResponse(_("Utilisateur non trouvé."), status=code)
    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def adminize_user(request, user_id=None):
    code, message = can_admin(request)
    if code == 200:
        if user_id:
            user_uuid = uuid.UUID(user_id, version=4)
            try:
                passed_user = Utilisateur.objects.get(id=user_uuid)
                if passed_user:
                    if passed_user == request.user :
                        messages.error(request, _("Vous ne pouvez pas rendre votre propre compte Admin."))
                        return redirect('tenancy_users')
                    passed_user.is_tenant_admin = True
                    passed_user.save()
            except Exception as xc:
                print(f"Error while enabling user with id {user_id}: {str(xc)}")
            messages.success(request, _("Utilisateur rendu Admin") + " : " + passed_user.username)

            return redirect('tenancy_users')

        return HttpResponse(_("Utilisateur non trouvé."), status=code)
    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def trial(request):
    code, message = can_admin(request)
    if code == 200:
        tenant = request.user.tenant

        subscriptions = Subscription.objects.filter(active=True, tenant=tenant)
        if subscriptions:
            messages.warning(request, _("Vous ne pouvez plus activer un Essai gratuit !"))
            return redirect('tenancy_summary')

        trials = Trial.objects.filter(active=True, tenant=tenant)
        if trials:
            messages.warning(request, _("Vous avez déjà bénéficié d'un Essai gratuit !"))
            return redirect('tenancy_summary')

        trial_date_start = today
        trial_date_end = today + timedelta(days=TRIAL_DAYS)
        plans = Plan.objects.filter(active=True).order_by('ordre')
        # plan = Plan.objects.filter(active=True).order_by('ordre').first()


        if request.method == "POST":
            plan_id = request.POST.get('plan_id', '')
            plan = Plan.objects.filter(id=plan_id).first()

            trial = Trial(
                    date_fm = trial_date_start,
                    date_to = trial_date_end,
                    tenant = tenant,
                    plan = plan,
            )
            try: 
                trial.save()
                messages.success(request, _("Votre période d'essai a commencé"))
            except Exception as xc: 
                messages.error(request, _("Quelque chose a mal tourné. Contacter le support."))
                print(str(xc))

            return redirect('tenancy_summary')
        else:
            context = {
                'trial_date_start' : trial_date_start,
                'trial_date_end'   : trial_date_end,
                'plans'            : plans,
                # 'plan'             : plan,
            }
            return render(request, 'tenancy/trial.html', context)

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def subscribe(request):
    code, message = can_admin(request)
    if code == 200:
        tenant = request.user.tenant
        context = {}
        subscriptions = Subscription.objects.filter(active=True, tenant=request.user.tenant).order_by('-date_to')
        latest_subscription = subscriptions.last()
        if not latest_subscription:
            context["repetition"] = "new"

        plans = Plan.objects.filter(active=True)
        context["high_plans"] = plans

        if latest_subscription:
            plan_ordre = latest_subscription.plan.ordre
            high_plans = plans.filter(ordre__gte=plan_ordre)
            periodicity = "yearly"
            start_date = today
            if latest_subscription.date_to <= latest_subscription.date_fm + timedelta(days=31):
                periodicity = "monthly"
            if latest_subscription.date_to > today :
                start_date = latest_subscription.date_to + relativedelta(days=1)
            end_date = start_date + relativedelta(years=1)
            if periodicity == "monthly":
                end_date = start_date + relativedelta(months=1)

            context["periodicity"]  = periodicity
            context["plans"]        = plans
            context["high_plans"]   = high_plans
            context["start_date"]   = start_date
            context["end_date"]     = end_date

        if request.method == "POST":
            plan_id = request.POST.get('plan_id', '')
            if plan_id != "":
                # messages.info(request, f"{plan_id}")
                plan_uuid = uuid.UUID(plan_id, version=4)
                selected_plan = Plan.objects.filter(active=True, id=plan_id).last()
                if latest_subscription:
                    if selected_plan:
                        if selected_plan.ordre < latest_subscription.plan.ordre:
                            dgd_message = _("Merci de séléctionner un Plan supérieur ou égal à celui de votre Abonnement précédent.")
                            messages.error(request, f"{dgd_message}")
                            return redirect("tenancy_summary")

                        return redirect("tenancy_order")
                        # plan_ordre = subscription.plan.ordre
                        # high_plans = plans.filter(ordre__gte=plan_ordre)
                        # periodicity = "yearly"
                        # start_date = today
                        # if subscription.date_to <= subscription.date_fm + timedelta(days=31):
                        #     periodicity = "monthly"
                        # if subscription.date_to > today :
                        #     start_date = subscription.date_to + relativedelta(days=1)
                        # end_date = start_date + relativedelta(years=1)
                        # if periodicity == "monthly":
                        #     end_date = start_date + relativedelta(months=1)

                        # context["periodicity"]  = periodicity
                        # context["plans"]        = plans
                        # context["high_plans"]   = high_plans
                        # context["start_date"]   = start_date
                        # context["end_date"]     = end_date

                        # return render(request, 'tenancy/subscribe.html', context)

                    sub_message = _("Votre Abonnement précédent n'a pas été trouvé.")
                    messages.error(request, f"{sub_message}")
                    return redirect("tenancy_summary")

                # New subscription
                periodicity = request.POST.get('periodicity', '')
                ###########################

                ###########################
                plan_message = f"Selected plan = { selected_plan.name } x { periodicity } | " + _("New Subscription: Coming soon.")
                # plan_message = _("Votre Plan précédent n'a pas été trouvé.")
                messages.error(request, f"{plan_message}")
                return redirect("tenancy_summary")

            sel_message = _("Votre séléction n'est pas valide.")
            messages.error(request, f"{sel_message}")
            return redirect("tenancy_summary")

        plans = Plan.objects.filter(active=True)
        context["plans"] = plans
        return render(request, 'tenancy/subscribe.html', context)

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def orders(request):

    code, message = can_admin(request)
    if code == 200:
        context = {}
        tenant = request.user.tenant
        s_orders = SystemOrder.objects.filter(customer=tenant).order_by('-order_date')
        context['orders'] = sorted(s_orders, key=lambda order: order.amount_due)
        # context['orders'] = s_orders

        return render(request, 'tenancy/orders.html', context)

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def order_create(request):

    code, message = can_admin(request)
    if code == 200:
        context = {}
        tenant = request.user.tenant
        # s_orders = SystemOrder.objects.filter(customer=tenant)
        # context['orders'] = s_orders

        return render(request, 'tenancy/orders.html', context)

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def order(request):

    code, message = can_admin(request)
    if code == 200:
        context = {}
        tenant = request.user.tenant

        subscriptions = Subscription.objects.filter(active=True, tenant=tenant)
        active_subscriptions = subscriptions.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_subscription = active_subscriptions.last()

        if not current_subscription:
            current_subscription = subscriptions.last()

        if current_subscription:

            start_date = today
            periodicity = "yearly"
            payments = SystemPayment.objects.filter(date_made__year=today.year)

            sub_delta = current_subscription.date_to - current_subscription.date_fm
            if sub_delta.days <= 31 : periodicity = "monthly"
            if current_subscription.date_to > today: start_date = current_subscription.date_to + relativedelta(days=1)
            end_date = start_date + relativedelta(months=1) if periodicity == "monthly" else start_date + relativedelta(years=1)
            plan = current_subscription.plan

            ht_amount    = plan.monthly_month_tag if periodicity == "monthly" else plan.yearly_year_tag
            taxes_amount = Decimal(ht_amount * plan.plan_taxes/100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_amount = Decimal(ht_amount + taxes_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            objet = _("Abonnement Annuel")
            if periodicity == "monthly":
                objet = _("Abonnement Mensuel")
            objet += f" - {plan.name} - {start_date} - {end_date}"

            if request.method == "POST":

                order_no = request.POST.get('order_no', '')
                # objet = request.POST.get('objet', '')
                # total_amount = request.POST.get('total_amount', '')

                paymt_no = order_no.replace("O", "P", 1)

                payment = SystemPayment(
                    order_no  = order_no,
                    date_made = today,
                    objet     = objet,
                    amount    = total_amount,
                    currency  = plan.currency,
                    reference = paymt_no,
                    made_by   = request.user,
                    note      = f"{tenant}-#{total_amount}#-{plan.name}-{today}"
                )
                try:
                    payment.save()
                except Exception as xc:
                    print(f"Error raised while creating System Payment: {str(xc)}")

                subscription = Subscription(
                    date_fm = start_date,
                    date_to = end_date,
                    tenant  = tenant,
                    plan    = plan,
                    payment = payment
                )
                try:
                    subscription.save()
                except Exception as xc:
                    print(f"Error raised while creating Subscription: {str(xc)}")

                pay_message = _("Abonnement activé. Merci de confirmer votre paiement.")
                messages.warning(request, f"{pay_message}")

                return redirect("tenancy_summary")
            else:
                year = today.year % 100
                day_of_year = today.timetuple().tm_yday
                order_no = f"SO-{year:02d}{day_of_year:03d}{1 + int(1 + len(payments)):05d}"

                context["order_no"]     = order_no
                context["objet"]        = objet
                context["periodicity"]  = periodicity
                context["ht_amount"]    = Decimal(ht_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                context["total_amount"] = total_amount
                context["taxes_amount"] = taxes_amount
                context["plan"]         = plan
                context["start_date"]   = start_date
                context["end_date"]     = end_date

                return render(request, 'tenancy/order.html', context)

        # New Subscription.

        nosub_message = _("Previous Subscription not found.")
        messages.error(request, f"{nosub_message}")

        return redirect("tenancy_summary")

    return HttpResponse(message, status=code)



@login_required(login_url="account_login")
def details(request):
    context = {}
    return render(request, 'tenancy/details.html', context)


@login_required(login_url="account_login")
def dashboard(request):
    context = {}
    return render(request, 'tenancy/dashboard.html', context)


@login_required(login_url="account_login")
def history(request):
    context = {}
    return render(request, 'tenancy/history.html', context)


@login_required(login_url="account_login")
def sub_cancel(request):
    context = {}
    return render(request, 'tenancy/sub-cancel.html', context)


@login_required(login_url="account_login")
def sub_upgrade(request):
    context = {}
    return render(request, 'tenancy/sub-upgrade.html', context)