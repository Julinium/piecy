from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from .models import Plan, Tenant, Subscription, Trial, SystemOrder, SystemOrderItem, SystemPayment

User = get_user_model()


class TenantAdmin(admin.ModelAdmin):
    model = Tenant
    list_display = ("name", "active", "city", "owner", 'created_on')
    fieldsets = (
        ("Basics", {"fields": ("active", "name", "owner")}),
        ("Contact", {"fields": ("email", "phone", "whatsapp", "address1", "address2", "city", "state", "country")}),
        ("Advanced", {"fields": ("domain_name", "channel", "note")}),
        ("History", {"fields": ('get_created_by', 'created_on', 'get_edited_by', 'edited_on')}),
    )

    add_fieldsets = fieldsets

    list_filter = ('active', 'created_on')
    search_fields = ('name', 'owner')
    ordering = ("active", 'name', 'city', 'owner', 'edited_on')

    readonly_fields = ('get_created_by', 'created_on', 'get_edited_by', 'edited_on')

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput},
    }
    
    def get_created_by(self, obj):
        return self._get_username(obj.created_by)
    get_created_by.short_description = 'Created by'

    def get_edited_by(self, obj):
        return self._get_username(obj.edited_by)
    get_edited_by.short_description = 'Edited by'

    def _get_username(self, user_id):
        try:
            return User.objects.get(pk=user_id).username
        except User.DoesNotExist:
            return f"(Deleted user: {user_id})" if user_id else "-"

    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by:
            obj.created_by = request.user
        else:
            obj.edited_by = request.user
        super().save_model(request, obj, form, change)


class PlanAdmin(admin.ModelAdmin):
    model = Plan

    list_display = ("name", "active", "monthly_price", 'header')

    readonly_fields = ('created_by', 'get_created_by', 'created_on', 'edited_by', 'get_edited_by', 'edited_on')

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput},
    }
    
    def get_created_by(self, obj):
        return self._get_username(obj.created_by)
    get_created_by.short_description = 'Created by'

    def get_edited_by(self, obj):
        return self._get_username(obj.edited_by)
    get_edited_by.short_description = 'Edited by'

    def _get_username(self, user_id):
        try:
            return User.objects.get(pk=user_id).username
        except User.DoesNotExist:
            return f"(Deleted user: {user_id})" if user_id else "-"

    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by:
            obj.created_by = request.user
        else:
            obj.edited_by = request.user
        super().save_model(request, obj, form, change)


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("username", "tenant", "email", "is_active", "last_login")
    readonly_fields = ('created_by', 'created_on', 'edited_by', 'edited_on', 'tenant', "username", "verified")

    fieldsets = (
        ("Basics",   {"fields": ("is_active", "is_tenant_admin", "username", "tenant")}),
        ("Personal", {"fields": ("first_name", "last_name", "email", "verified", "phone")}),
        # ("Security", {"fields": ("verified")}),
        # ("Advanced", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    
    add_fieldsets = (
        # (None, {
        #     # "classes": ("wide",),
        #     "fields": ("username", "email", "password1", "password2", "", "")}
        # ),
        ("Basics",   {"fields": ("is_active", "tenant", "is_tenant_admin", "username", "password1", "password2")}),
        ("Personal", {"fields": ("first_name", "last_name", "email", "phone")}),
        
    )

    search_fields = ("username", "email", "last_name")
    ordering = ('-is_active', '-tenant', 'created_on', 'last_login', 'is_tenant_admin',)

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput},
    }

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []  # No read-only fields for new instances


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription


class TrialAdmin(admin.ModelAdmin):
    model = Trial


class SystemOrderItemInline(admin.TabularInline):  # or admin.StackedInline
    model = SystemOrderItem
    extra = 1


class SystemOrderAdmin(admin.ModelAdmin):
    model = SystemOrder
    list_display = ("order_number", 'total_amount_with_tax', "customer", "status")
    list_filter = ('status',)
    inlines = [SystemOrderItemInline]


class SystemOrderItemAdmin(admin.ModelAdmin):
    model = SystemOrderItem


class SystemPaymentAdmin(admin.ModelAdmin):
    model = SystemPayment
    list_display = ('reference', 'amount', 'status', 'paid_at')
    list_filter = ('status', 'paid_at')

    actions = ['set_status_confirmed', 'set_status_pending', 'set_status_failed']
    def set_status_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    set_status_confirmed.short_description = "Confirm Selected"
    def set_status_pending(self, request, queryset):
        queryset.update(status='pending')
    set_status_pending.short_description = "Unconfirm Selected"
    def set_status_failed(self, request, queryset):
        queryset.update(status='failed')
    set_status_failed.short_description = "Fail Selected"



admin.site.register(Tenant, TenantAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Trial, TrialAdmin)
admin.site.register(SystemOrder, SystemOrderAdmin)
admin.site.register(SystemOrderItem, SystemOrderItemAdmin)
admin.site.register(SystemPayment, SystemPaymentAdmin)
