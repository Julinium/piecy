from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ("username", "email", "tenant", "is_tenant_admin", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "tenant")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("username", "email", "tenant", "last_name")
    ordering = ("username",)

admin.site.register(Utilisateur, UtilisateurAdmin)
