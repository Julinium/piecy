from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from back.models import Tenant

class TenantAdmin(admin.ModelAdmin):
    model = Tenant
    ###################
    # active = models.BooleanField(blank=True, null=True, default=True)
    # name = models.CharField(max_length=128, blank=True, null=True)
    # email = models.CharField(max_length=16, blank=True, null=True)
    # address = models.CharField(max_length=64, blank=True, null=True)
    # phone = models.CharField(max_length=16, blank=True, null=True)
    # whatsapp = models.CharField(max_length=16, blank=True, null=True)
    # domain = models.CharField(max_length=32, blank=True, null=True)
    # slug = models.CharField(max_length=32, blank=True, null=True)
    # owner = models.CharField(max_length=64, blank=True, null=True)
    # channel = models.CharField(max_length=32, blank=True, null=True)
    # note = models.CharField(max_length=256, blank=True, null=True)

    # owned_by = models.UUIDField(blank=True, null=True)
    # created_by = models.UUIDField(blank=True, null=True)
    # created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    # edited_by = models.UUIDField(blank=True, null=True)
    # edited_on = models.DateTimeField(blank=True, null=True, auto_now=True)
    ###################
    list_display = ("name", "active", "address", "owner", "note", 'created_on', 'created_by', 'edited_on', 'edited_by')
    fieldsets = (
        ("Basics", {"fields": ("active", "name", "owner")}),
        ("Contact", {"fields": ("email", "phone", "whatsapp", "address")}),
        ("Advanced", {"fields": ("domain", "slug", "channel", "note")}),
    )

    # add_fieldsets = (
    #     (None, {
    #         "classes": ("wide",),
    #         "fields": ("username", "email", "password1", "password2", "is_staff", "is_active")}
    #     ),
    # )

    add_fieldsets = fieldsets

    list_filter = ('active', 'created_on')
    search_fields = ('name', 'owner')
    ordering = ("active", 'name', 'owner', 'edited_on')

    def save_model(self, request, obj, form, change):
        # if not change:
        if not change or not obj.created_by:
            obj.created_by = request.user.id
        else:
            obj.edited_by = request.user.id
        super().save_model(request, obj, form, change)

admin.site.register(Tenant, TenantAdmin)
