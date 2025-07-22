from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.utils.text import capfirst
from back.models import Tenant


@login_required(login_url="account_login")
def tenant(request):
    user = request.user
    if user:
        if user.is_active:
            tenant = user.tenant
            if tenant:
                if tenant.active:
                    fields = [(capfirst(field.verbose_name), getattr(tenant, field.name)) for field in tenant._meta.fields]
                    admins = tenant.workers.filter(is_tenant_admin = True)#.order_by("-is_active")
                    workers = tenant.workers.exclude(is_tenant_admin = True)#.order_by("-is_active")
                    context = { "tenant" : tenant, "fields" : fields, "admins" : admins, "workers" : workers }
                    return render(request, 'tenancy/tenancy-detail.html', context)
                
                return HttpResponse(_('Tenant inactive'), status=403)
            return HttpResponse(_('Tenant not found !'), status=404)
        return HttpResponse(_('User inactive'), status=403)
    return HttpResponse(_('User not found!'), status=404)
    