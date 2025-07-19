from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from back.models import Plan, Tenant, SystemPayment, Subscription

User = get_user_model()


class TenantAdmin(admin.ModelAdmin):
    model = Tenant
    list_display = ("name", "active", "address", "owner", 'created_on')
    fieldsets = (
        ("Basics", {"fields": ("active", "name", "owner")}),
        ("Contact", {"fields": ("email", "phone", "whatsapp", "address")}),
        ("Advanced", {"fields": ("domain", "slug", "channel", "note")}),
        ("History", {"fields": ('get_created_by', 'created_on', 'get_edited_by', 'edited_on')}),
    )

    add_fieldsets = fieldsets

    list_filter = ('active', 'created_on')
    search_fields = ('name', 'owner')
    ordering = ("active", 'name', 'address', 'owner', 'edited_on')

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
            obj.created_by = request.user.id
        else:
            obj.edited_by = request.user.id
        super().save_model(request, obj, form, change)


class PlanAdmin(admin.ModelAdmin):
    model = Plan

    # list_display = ("name", "active", "address", "owner", 'created_on')
    # fieldsets = (
    #     ("Basics", {"fields": ("active", "name", "owner")}),
    #     ("Contact", {"fields": ("email", "phone", "whatsapp", "address")}),
    #     ("Advanced", {"fields": ("domain", "slug", "channel", "note")}),
    #     ("History", {"fields": ('get_created_by', 'created_on', 'get_edited_by', 'edited_on')}),
    # )

    # add_fieldsets = fieldsets

    readonly_fields = ('owned_by', 'created_by', 'get_created_by', 'created_on', 'edited_by', 'get_edited_by', 'edited_on')

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
            obj.created_by = request.user.id
        else:
            obj.edited_by = request.user.id
        super().save_model(request, obj, form, change)

class SystemPaymentAdmin(admin.ModelAdmin):
    model = SystemPayment


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription



admin.site.register(Tenant, TenantAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(SystemPayment, SystemPaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
