from django import forms
from .models import MaintenanceReport


class LoginForm(forms.Form):
    emp_number = forms.CharField(max_length=8, required=True)
    captcha = forms.CharField(max_length=6, required=True)
