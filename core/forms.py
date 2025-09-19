from django import forms
from .models import Customer, Account

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address', 'profile_picture']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'currency']
