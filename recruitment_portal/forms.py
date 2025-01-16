from django import forms
from .models import *



class RegistrationForm(forms.Form):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('poc', 'POC'),
    ]

    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    name = forms.CharField(max_length=255, required=True)
