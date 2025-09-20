from django import forms
from core.models import Customer # Import Customer from core

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Textarea, forms.Select)):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs['class'] = 'form-control-file'