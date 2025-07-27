import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
# from datetime import date, datetime, timedelta, timezone
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.contrib import messages

from decimal import Decimal, ROUND_HALF_UP

from django.http import HttpResponse
# from django.utils.text import capfirst
from back.models import SystemPayment, Plan, Subscription


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
        active_subscriptions  = subscriptions.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to', 'is_trial')
        current_subscription = active_subscriptions.last()
    
        can_try = False if subscriptions else True

        days_remaining = 0
        if current_subscription:
            delta = current_subscription.date_to - today
            days_remaining = delta.days
            if current_subscription.is_trial: 
                # messages.error(request, _("Période d'essai. Merci de souscrire un abonnement."))
                messages.error(request, _("Jours d'essai restant") + f" : {days_remaining}")
        # else:
            # messages.error(request, _("Aucun abonnement actif. Contacter nous."))

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
def subscribe(request):
    code, message = can_admin(request)
    if code == 200:
        plans = Plan.objects.filter(active=True)
        context = {
            "plans" : plans,
        }
        return render(request, 'tenancy/subscribe.html', context)

    return HttpResponse(message, status=code)



@login_required(login_url="account_login")
def order(request):
    code, message = can_admin(request)
    if code == 200:
        if request.method == "POST":
            stage = request.POST.get('stage', '')
            plan_id = request.POST.get('plan_id', '')
            tag = request.POST.get('tag', '')
            tag_new = request.POST.get('tag_new', '')
            period = request.POST.get('period', '')

            plan_uuid = uuid.UUID(plan_id, version=4)
            plan = Plan.objects.filter(id=plan_uuid).first()
            tenant=request.user.tenant

            subs = Subscription.objects.filter(active=True, is_trial=False, tenant=tenant).order_by('date_fm')
            is_new = True if len(subs) == 0 else False

            periodicity = "1" if period == "monthly" else "12"
            monthly_price = int(tag_new) if is_new else  int(tag)

            price_normal = plan.monthly_price if period == "monthly" else 12 * plan.monthly_price
            discount_new = True if is_new else False
            price = monthly_price if period == "monthly" else 12 * monthly_price
            discount_year = False if period == "monthly" else True
            
            taxes_amount = Decimal(price * plan.plan_taxes/100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_amount = Decimal(price + taxes_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            start_date = today
            sub = subs.last()
            if sub: 
                start_date = sub.date_to + relativedelta(days=1)
            end_date = start_date + relativedelta(months=1) if period == "monthly" else start_date + relativedelta(years=1)

            if stage == "selection":
                ctx = {
                    "monthly_price" : Decimal(monthly_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                    "price"         : Decimal(price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                    "price_normal"  : Decimal(price_normal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                    "periodicity"   : periodicity + " " + _("Mois"),
                    "plan"          : plan,
                    "tag"           : tag,
                    "tag_new"       : tag_new,
                    "start_date"    : start_date,
                    "end_date"      : end_date,
                    "discount_new"  : discount_new,
                    "discount_year" : discount_year,
                    "taxes_amount"  : taxes_amount,
                    "total_amount"  : total_amount,
                }
                return render(request, 'tenancy/order.html', ctx)

            else:
                payments = SystemPayment.objects.filter(date_made__year=today.year)
                year = today.year % 100
                day_of_year = today.timetuple().tm_yday
                order_no = f"SO-{year:02d}{day_of_year:03d}{1 + int(1 + len(payments)):05d}"
                paymt_no = f"SP-{year:02d}{day_of_year:03d}{1 + int(1 + len(payments)):05d}"

                
                payment = SystemPayment(
                    order_no    = order_no,
                    date_made   = today,
                    amount      = total_amount,
                    currency    = plan.currency,
                    reference   = paymt_no,
                    made_by     = request.user,
                    note        = f"{tenant}-{plan.name}-{today}"
                )
                try:
                    payment.save()
                except Exception as xc:
                    print(f"Error raised while creating System Payment: {str(xc)}")
                
                all_subscriptions  = Subscription.objects.filter(tenant=tenant)
                subscriptions = all_subscriptions.filter(active=True)
                active_subscriptions  = subscriptions.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to', 'is_trial')
                current_subscription = active_subscriptions.last()
                if current_subscription:
                    if current_subscription.is_trial:
                        subscription = current_subscription
                        subscription.date_fm = start_date
                        subscription.date_to = end_date
                        subscription.tenant  = tenant
                        subscription.plan    = plan
                        subscription.payment = payment
                        subscription.is_trial = False
                else:
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

                pay_message = _("Merci de confirmer votre payment.")
                messages.warning(request, f"{pay_message}")

            return redirect("tenancy_summary")


        context = {}
        return render(request, 'tenancy/order.html', context)

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