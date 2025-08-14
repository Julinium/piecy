import secrets, string
from django.utils.translation import gettext as _

from django import forms
from django.contrib.auth import get_user_model
# from back.models import SystemPayment

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_tenant_admin']

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class'      : 'form-control', 
                'required'   : 'true',
                'minlength'  : '2',
                'maxlength'  : '16',
                'pattern'    : "[A-Za-z0-9._@- ]*",
                'id'         : 'first_name_input',
                }),


            'last_name': forms.TextInput(attrs={
                'class'      : 'form-control', 
                'required'   : 'true',
                'minlength'  : '2',
                'maxlength'  : '16',
                'pattern'    : "[A-Za-z0-9._@- ]*",
                'id'         : 'last_name_input',
                }),


            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'required'   : 'true',
                'minlength'  : '4',
                'maxlength'  : '16',
                'pattern'    : "[a-z][A-Za-z0-9._@-]*",
                'id': 'username_input',
                }),


            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'id': 'email_input', 
                }),


            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 
                'id': 'is_active_input'
                }),


            'is_tenant_admin': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 
                'id': 'is_tenant_admin_input'
                }),
        }
