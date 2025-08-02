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
from back.models import SystemPayment, Plan, Subscription, Trial


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
        tenant_admins = tenant.workers.filter(is_tenant_admin = True)
        tenant_users = tenant.workers.exclude(is_tenant_admin = True)

        context = {
            "tenant" : tenant,
            "admins" : tenant_admins,
            "users"  : tenant_users,
        }

        subscriptions         = Subscription.objects.filter(tenant=tenant, active=True)
        running_subscriptions = subscriptions.filter(date_fm__lte=today, date_to__gte=today).order_by('date_to')
        current_subscription  = running_subscriptions.last()
        
        if subscriptions:
            context ["box"] = "S1R0"
            context ["subscriptions"] = subscriptions
            subscription_remaining_days = 0
            latest_subscription = subscriptions.latest('date_to')
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
            subs_id = request.POST.get('subs_id', '')
            if subs_id != "":
                subscription = Subscription.objects.filter(active=True, id=subs_id).last()
                if subscription:
                    plan_ordre = subscription.plan.ordre
                    # plans = Plan.objects.filter(active=True)
                    high_plans = plans.filter(ordre__gte=plan_ordre)
                    periodicity = "yearly"
                    start_date = today
                    if subscription.date_to <= subscription.date_fm + timedelta(days=31):
                        periodicity = "monthly"
                    if subscription.date_to > today :
                        start_date = subscription.date_to + relativedelta(days=1)
                    end_date = start_date + relativedelta(years=1)
                    if periodicity == "monthly":
                        end_date = start_date + relativedelta(months=1)

                    context["periodicity"]  = periodicity
                    context["plans"]        = plans
                    context["high_plans"]   = high_plans
                    context["start_date"]   = start_date
                    context["end_date"]     = end_date

                    return render(request, 'tenancy/subscribe.html', context)
            return HttpResponse("Something went wrong !", status=503)

        plans = Plan.objects.filter(active=True)
        context["plans"] = plans
        return render(request, 'tenancy/subscribe.html', context)

    return HttpResponse(message, status=code)



@login_required(login_url="account_login")
def order(request):
    # TODO: Handle downgrading
    # Expected params:
        # Tenant <- user <- request
        # Amount (before taxes ?)
        # Plan -> Currency, ->
        # Start and End date

                            # <input type="hidden" name="subs_id" value="{{ latest_subscription.id }}">
                            # <input type="hidden" name="box" value="S1R0">

    code, message = can_admin(request)
    if code == 200:
        context = {}
        if request.method == "POST":

            subscription_id = request.POST.get('subscription_id', '')
            stage = request.POST.get('stage', '')
            box = request.POST.get('box', '')
            
            subscription_uuid = uuid.UUID(subscription_id, version=4)
            latest_subscription = Subscription.objects.filter(active=True, id=subscription_uuid)


###############################



            # box = request.POST.get('box', '')
            # if box == "S1R0":
            #     subs_id = request.POST.get('subs_id', '')
            #     subscription = Subscription.objects.filter(active=True, id=subs_id).last()
            #     start_date = today
                # if subscription:
                #     if subscription.date_to:
                        # Select period
                        # Select eventually Plan


                    # context["subscription"] = subscription





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
def x_order(request):
    # TODO: Handle downgrading
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