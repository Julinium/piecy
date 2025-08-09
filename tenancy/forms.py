# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from back.models import Utilisateur

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text=_(""))

    class Meta:
        model = Utilisateur
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
