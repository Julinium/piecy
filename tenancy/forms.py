# import secrets, string
from django.utils import timezone

from django.utils.translation import gettext as _

from django import forms
from django.contrib.auth import get_user_model
from back.models import SystemPayment

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


class SystemPaymentForm(forms.ModelForm):
    class Meta:
        model = SystemPayment
        fields = ['amount', 'method', 'reference', 'paid_at', 'notes']

        widgets = {
            'amount': forms.NumberInput(attrs={
                "class": "form-control text-end",
                'id'   : 'amount_input',
                "step" : "0.01",
                "min"  : "0",
            }),
            'paid_at': forms.DateTimeInput(attrs={
                'class'    : 'form-control text-end', 
                "type"     : "datetime-local",
                "value"    : "2025-08-20T20:15",
                'required' : 'true',
                'id'       : 'paid_at_input',
                },
                format="%Y-%m-%dT%H:%M",
                ),
            'notes': forms.Textarea(attrs={
                "class": "form-control",
                'id'   : 'notes_input',
                'rows' : 3,
            }),
            'method': forms.Select(attrs={
                "class": "form-control",
                'id'   : 'method_input',
            }),
            'reference': forms.TextInput(attrs={
                "class": "form-control",
                'id'   : 'reference_input',
            }),
        }

        # numero = models.CharField(max_length=20, unique=True, editable=False)
        #  = models.DecimalField(max_digits=10, decimal_places=2)
        #  = models.CharField(max_length=20, choices=METHOD_CHOICES)
        # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
        # reference = models.CharField(max_length=100, blank=True)
        # paid_at = models.DateTimeField(null=True, blank=True)
        # notes = models.TextField(blank=True)