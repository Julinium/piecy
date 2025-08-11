# import uuid
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
# from back.models import Utilisateur, Tenant

# forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Mot de passe')}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirmation Mot de passe')}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_tenant_admin']  # tenant excluded

        widgets = {

            # <input type="email" class="form-control" id="floatingInputValue" placeholder="name@example.com" value="test@example.com">
            # <label for="floatingInputValue">Input with value</label>

            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name_input', 'placeholder': _('Prénom')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name_input', 'placeholder': _('Nom')}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username_input', 'placeholder': _('Nom Utilisateur')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email_input', 'placeholder': _('Email')}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active_input'}),
            'is_tenant_admin': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_tenant_admin_input'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





# class X_CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True, help_text=_("Entrer une adresse email valide"))
#     tenant = forms.CharField(required=True, label=_("Entreprise"))

#     class Meta:
#         model = Utilisateur
#         fields = ("username", "email", "password1", "password2")
#         # fields = ("tenant", "username", "email", "password1", "password2")

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user

#     def __init__(self, *args, **kwargs):
#         tenant_value = kwargs.pop("tenant", None)
#         super().__init__(*args, **kwargs)

#         for field in self.fields.values():
#             existing_classes = field.widget.attrs.get('class', '')
#             field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

#         # Set value + readonly
#         if tenant_value is not None:
#             # tenant_uuid = uuid.UUID(tenant_value, version=4)
#             # tenant = Tenant.objects.filter(id=tenant_uuid).last()
#             tenant = Tenant.objects.filter(id=tenant_value).last()
#             self.initial["tenant"] = tenant.id
#         if "tenant" in self.fields:
#             self.fields["tenant"].widget.attrs["readonly"] = True

#             existing_classes = self.fields["tenant"].widget.attrs.get('class', '')
#             self.fields["tenant"].widget.attrs['class'] = (existing_classes + ' fw-bold text-success bg-secondary-subtle').strip()
        