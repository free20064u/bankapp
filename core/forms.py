from django import forms
from .models import Account, Transaction

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'currency']

class TransactionForm(forms.ModelForm):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'), # Added transfer type
    ]
    transaction_type = forms.ChoiceField(choices=TRANSACTION_TYPES)
    # Added recipient_account for transfers
    recipient_account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        empty_label="Select Recipient Account (for transfers)"
    )

    class Meta:
        model = Transaction
        fields = ['account', 'amount', 'description'] # 'account' here is the sender's account

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Pop the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Filter the 'account' field to only show accounts belonging to the current user
            self.fields['account'].queryset = user.customer.account_set.all()
            # Filter the 'recipient_account' field to exclude the sender's accounts initially
            # and allow selection of any other account in the system for transfers
            self.fields['recipient_account'].queryset = Account.objects.exclude(customer=user.customer)

        # Add Bootstrap form-control class to fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Textarea, forms.Select)):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs['class'] = 'form-control-file'

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        account = cleaned_data.get('account')
        amount = cleaned_data.get('amount')
        recipient_account = cleaned_data.get('recipient_account')

        if transaction_type == 'transfer':
            if not recipient_account:
                self.add_error('recipient_account', "Recipient account is required for transfers.")
            if account and recipient_account and account.currency != recipient_account.currency:
                self.add_error('recipient_account', "Cannot transfer between accounts of different currencies.")
            if account and recipient_account and account == recipient_account:
                self.add_error('recipient_account', "Cannot transfer to the same account.")

        if amount and amount <= 0:
            self.add_error('amount', "Amount must be positive.")

        return cleaned_data