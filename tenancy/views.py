from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.utils.text import capfirst
from back.models import Tenant, Utilisateur


@login_required(login_url="account_login")
def summary(request):
    user = request.user
    if user:
        if user.is_active:
            tenant = user.tenant
            if tenant:
                # if tenant.active:
                fields = [(capfirst(field.verbose_name), getattr(tenant, field.name)) for field in tenant._meta.fields]
                admins = tenant.workers.filter(is_tenant_admin = True)#.order_by("-is_active")
                users = tenant.workers.exclude(is_tenant_admin = True)#.order_by("-is_active")

                # Subscription status
                # General required action: None, Renew, Upgrade, 

                context = { 
                    "tenant"   : tenant, 
                    "fields"   : fields, 
                    "admins"   : admins, 
                    "users"    : users
                }
                return render(request, 'tenancy/summary.html', context)
                
                # return HttpResponse(_('Tenant inactive'), status=403)
            return HttpResponse(_('Tenant not found !'), status=404)
        return HttpResponse(_('User inactive'), status=403)
    return HttpResponse(_('User not found!'), status=404)




@login_required(login_url="account_login")
def details(request):
    context = {}
    return render(request, 'tenancy/details.html', context)


@login_required(login_url="account_login")
def users(request):
    context = {}
    return render(request, 'tenancy/users.html', context)


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