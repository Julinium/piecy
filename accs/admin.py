from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    model = Utilisateur

    list_display = ("username", "is_active", "email", "tenant", "is_tenant_admin")
    
    fieldsets = (
        ("Basics",   {"fields": ("is_active", "is_tenant_admin", "username", "password", "tenant")}),
        ("Personal", {"fields": ("first_name", "last_name", "email", "phone")}),
        # ("Security", {"fields": ("verified")}),
        ("Advanced", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    
    add_fieldsets = (
        # (None, {
        #     # "classes": ("wide",),
        #     "fields": ("username", "email", "password1", "password2", "", "")}
        # ),
        ("Basics",   {"fields": ("is_active", "tenant", "is_tenant_admin", "username", "password1", "password2")}),
        ("Personal", {"fields": ("first_name", "last_name", "email", "phone")}),
        
    )

    # add_fieldsets = (
    #     (None, {
    #         "classes": ("wide",),
    #         "fields": ("username", "email", "password1", "password2", "is_staff", "is_active")}
    #     ),
    # )

    search_fields = ("username", "email", "last_name")
    # ordering = ("username", "tenant",)
    ordering = ('-is_active', '-tenant', 'created_on', 'last_login', 'is_tenant_admin',)

    formfield_overrides = {
        models.BooleanField: {'widget': forms.CheckboxInput},
    }

admin.site.register(Utilisateur, UtilisateurAdmin)
