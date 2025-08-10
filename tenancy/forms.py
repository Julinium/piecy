import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from back.models import Utilisateur, Tenant

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text=_("Entrer une adresse email valide"))
    tenant = forms.CharField(required=True, label=_("Entreprise"))

    class Meta:
        model = Utilisateur
        fields = ("username", "email", "password1", "password2")
        # fields = ("tenant", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        tenant_value = kwargs.pop("tenant", None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

        # Set value + readonly
        if tenant_value is not None:
            # tenant_uuid = uuid.UUID(tenant_value, version=4)
            # tenant = Tenant.objects.filter(id=tenant_uuid).last()
            tenant = Tenant.objects.filter(id=tenant_value).last()
            self.initial["tenant"] = tenant.id
        if "tenant" in self.fields:
            self.fields["tenant"].widget.attrs["readonly"] = True

            existing_classes = self.fields["tenant"].widget.attrs.get('class', '')
            self.fields["tenant"].widget.attrs['class'] = (existing_classes + ' fw-bold text-success bg-secondary-subtle').strip()