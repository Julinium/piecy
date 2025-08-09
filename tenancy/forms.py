# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from back.models import Utilisateur

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text=_("Entrer une adresse email valide"))
    tenant = forms.CharField(required=True, label=_("Entreprise"))

    class Meta:
        model = Utilisateur
        fields = ("tenant", "username", "email", "password1", "password2")

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
            self.initial["tenant"] = tenant_value
        if "tenant" in self.fields:
            self.fields["tenant"].widget.attrs["readonly"] = True