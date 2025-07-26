from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
# from datetime import date, datetime, timedelta, timezone
from datetime import timedelta
from django.contrib import messages
from django.utils.timezone import now

from django.http import HttpResponse
# from django.utils.text import capfirst
from back.models import Tenant, Plan, Utilisateur, Subscription


SUB_DAYS_WARNING = 90
SUB_DAYS_DANGER = 30

TRIAL_DAYS = 30

today = now().date()


def can_admin(request) -> tuple[int, str]:
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



@login_required(login_url="account_login")
def summary(request):
    code, message = can_admin(request)
    if code == 200:
        tenant = request.user.tenant

        admins = tenant.workers.filter(is_tenant_admin = True)
        users = tenant.workers.exclude(is_tenant_admin = True)

        all_subscriptions  = Subscription.objects.filter(tenant=tenant)
        subscriptions = all_subscriptions.filter(active=True)
        active_subscriptions  = subscriptions.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_subscription = active_subscriptions.last()
        
        can_try = False if subscriptions else True

        days_remaining = 0
        if current_subscription:
            delta = current_subscription.date_to - today
            days_remaining = delta.days
            if current_subscription.is_trial: 
                messages.error(request, _("Période d'essai. Merci de souscrire un abonnement."))
                messages.error(request, _("Jours d'essai restant") + f" : {days_remaining}")
        else:
            messages.error(request, _("Aucun abonnement actif. Contacter nous."))

        trial_percentage = 0
        if TRIAL_DAYS != 0: trial_percentage = min(100, int(100 * days_remaining/TRIAL_DAYS))

        tint = 'secondary'
        if days_remaining >= SUB_DAYS_WARNING: tint = "success"
        elif SUB_DAYS_DANGER <= days_remaining < 90: tint = "warning"
        elif 0 <= days_remaining < SUB_DAYS_DANGER: tint = "danger"


        # Subscription status
        # General required action: None, Renew, Upgrade, 

        context = { 
            "tenant"               : tenant, 
            "days_remaining"       : days_remaining, 
            "trial_percentage"     : trial_percentage, 
            "active_subscriptions" : active_subscriptions, 
            "current_subscription" : current_subscription, 
            "can_try"              : can_try,
            "tint"                 : tint, 
            "admins"               : admins, 
            "users"                : users
        }

        return render(request, 'tenancy/summary.html', context)
    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def trial(request):
    code, message = can_admin(request)
    if code == 200:
        tenant = request.user.tenant

        trial_date_start = today
        trial_date_end = today + timedelta(days=TRIAL_DAYS)
        plan = Plan.objects.filter(active=True).order_by('ordre').first()

        if request.method == "POST":
            subscription = Subscription(
                    is_trial = True,
                    date_fm = trial_date_start,
                    date_to = trial_date_end,
                    tenant = tenant,
                    plan = plan,
            )
            try: 
                subscription.save()
                messages.success(request, _("Votre période d'essai a commencé"))
            except Exception as xc: 
                messages.error(request, _("Quelque chose a mal tourné. Contacter le support."))
                print(str(xc))

            return redirect('tenancy_summary')
        else:
            context = {
                'trial_date_start' : trial_date_start,
                'trial_date_end'   : trial_date_end,
                'plan'             : plan,
            }
            return render(request, 'tenancy/trial.html', context)

    return HttpResponse(message, status=code)


@login_required(login_url="account_login")
def sub_renew(request):
    code, message = can_admin(request)
    if code == 200:
        if request.method == "POST":
            plan_id = request.POST.get('plan_id', '')
            tag = request.POST.get('tag', '')
            period = request.POST.get('period', '')
            messages.success(request, f"POST returned period = {period}, tag = {tag} and plan = {plan_id}")
            return redirect("tenancy_summary")

        plans = Plan.objects.filter(active=True)
        context = {
            "plans" : plans,
        }
        return render(request, 'tenancy/sub-renew.html', context)

    return HttpResponse(message, status=code)



@login_required(login_url="account_login")
def users(request):
    context = {}
    return render(request, 'tenancy/users.html', context)


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