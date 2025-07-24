from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
# from datetime import date, datetime, timedelta, timezone
from datetime import timedelta
from django.utils.timezone import now

from django.http import HttpResponse
# from django.utils.text import capfirst
from back.models import Tenant, Utilisateur, Subscription


SUB_DAYS_WARNING = 90
SUB_DAYS_DANGER = 30

TRIAL_DAYS = 30

today = now().date()

@login_required(login_url="account_login")
def summary(request):
    user = request.user
    if user:
        if user.is_active:
            tenant = user.tenant
            if tenant:
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

                tint = 'secondary'
                if days_remaining >= SUB_DAYS_WARNING: tint = "success"
                elif SUB_DAYS_DANGER <= days_remaining < 90: tint = "warning"
                elif 0 <= days_remaining < SUB_DAYS_DANGER: tint = "danger"


                # Subscription status
                # General required action: None, Renew, Upgrade, 

                context = { 
                    "tenant"               : tenant, 
                    "days_remaining"       : days_remaining, 
                    "active_subscriptions" : active_subscriptions, 
                    "current_subscription" : current_subscription, 
                    "can_try"              : can_try,
                    "tint"                 : tint, 
                    "admins"               : admins, 
                    "users"                : users
                }

                return render(request, 'tenancy/summary.html', context)                
            return HttpResponse(_('Tenant not found !'), status=404)
        return HttpResponse(_('User inactive'), status=403)
    return HttpResponse(_('User not found!'), status=404)



@login_required(login_url="account_login")
def trial(request):    
    user = request.user
    if user:
        if user.is_active:
            tenant = user.tenant
            if tenant:
                trial_date_start = today
                trial_date_end = today + timedelta(days=TRIAL_DAYS) 
                
                context = {
                    'trial_date_start' : trial_date_start,
                    'trial_date_end'   : trial_date_end,
                }
                return render(request, 'tenancy/trial.html', context)



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
def sub_renew(request):
    context = {}
    return render(request, 'tenancy/sub-renew.html', context)


@login_required(login_url="account_login")
def sub_upgrade(request):
    context = {}
    return render(request, 'tenancy/sub-upgrade.html', context)