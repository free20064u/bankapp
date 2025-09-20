from django import forms
from django.contrib.auth.models import User
from core.models import Customer

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
